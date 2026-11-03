"""计费 / 计税引擎：带生效时间的版本化规则 + 可组合的规则链 + 金额只在边界取整一次。

三个想法撑起整个设计：
1. 版本：每个商户的规则按"生效时间"排成升序的版本，`quote` 用二分找到交易发生那一刻生效的版本，
   而不是当前配置——这样一个月前的交易今天重算，数字一模一样；
2. 规则链：每条规则是一个对象，统一接口 `apply(txn, prior) -> Decimal | None`，引擎只负责按顺序跑，
   后面的规则看得到前面已经取整的各行（税建在费用之上）。加一种费用或一种税，只新增规则对象，不改引擎；
3. 取整：规则内部用 `Decimal` 全精度，引擎在每一行产出时调用唯一的 `_to_minor` 取整一次（银行家舍入）。
   所以任何一行金额都能凭"规则 ID + 版本号"精确复现。

发布用"复制后替换"：每个商户的版本表是一个不可变快照 `_Schedule`，`publish` 在锁里造出新快照再换引用，
`quote` 读到的永远是完整的某一版，读路径不加锁。
"""

from __future__ import annotations

import threading
from bisect import bisect_right
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from decimal import ROUND_HALF_EVEN, Decimal
from typing import Protocol


class BillingError(Exception):
    """引擎所有失败路径的公共基类。"""


class NoActiveRules(BillingError, LookupError):
    """交易发生时，该商户没有任何生效的规则版本。宁可报错，也不能悄悄按 0 收费。"""


class StaleVersion(BillingError, ValueError):
    """新版本的生效时间必须严格晚于该商户上一个版本。历史靠发布新版本加调整行来修正，不改旧版本。"""


class InvalidRuleSet(BillingError, ValueError):
    """规则集不合法：ID 重复、依赖了不存在的规则、依赖成环、阶梯定义不合法。"""


class MissingCurrency(BillingError, LookupError):
    """规则没有为交易的币种配置固定费。"""


@dataclass(frozen=True, slots=True)
class Txn:
    id: str
    merchant: str
    amount: int          # 最小货币单位（分）
    currency: str
    ts: int              # 交易发生的时间（epoch 秒）；永远不用"处理时间"


@dataclass(frozen=True, slots=True)
class Line:
    rule_id: str
    kind: str            # "fee"、"tax" 或 "adjustment"：税规则按 kind 汇总，不靠名字猜
    version: int
    amount: int          # 整数最小货币单位


class Rule(Protocol):
    """一条规则只需要会一件事：看交易和前面各行，给出全精度金额，或者"不适用"。结构化类型，不必继承。"""

    rule_id: str
    kind: str
    needs: tuple[str, ...]      # 必须排在它前面的规则 ID（第 3 关）

    def apply(self, txn: Txn, prior: tuple[Line, ...]) -> Decimal | None: ...


def _to_minor(x: Decimal) -> int:
    """全系统唯一的取整点：银行家舍入（遇 0.5 取偶数），一行只取整一次。"""
    return int(x.quantize(Decimal(1), rounding=ROUND_HALF_EVEN))


def _bps(amount: int | Decimal, bps: int) -> Decimal:
    return Decimal(amount) * bps / 10_000


# ---- 第 1 关：版本、规则链、取整 ----------------------------------------------


@dataclass(frozen=True, slots=True)
class PercentPlusFixed:
    """费用 = 金额 x 费率 + 固定费。`fixed` 可以是一个整数，或 {币种: 固定费}（第 3 关）。"""

    rule_id: str
    bps: int                                    # 290 表示 2.9%
    fixed: int | Mapping[str, int] = 0
    kind: str = "fee"
    needs: tuple[str, ...] = ()

    def apply(self, txn: Txn, prior: tuple[Line, ...]) -> Decimal | None:
        """金额不是正数时不适用（返回 None）；固定费缺该币种时抛 MissingCurrency。"""
        if txn.amount <= 0:
            return None
        return _bps(txn.amount, self.bps) + _fixed_for(self.fixed, txn.currency)


@dataclass(frozen=True, slots=True)
class TaxOnFees:
    """税 = 前面各行里 kind 为 "fee" 的金额合计 x 税率。税看到的是已经取整的费用行，账面上每行相加就是总数。"""

    rule_id: str
    bps: int
    kind: str = "tax"
    needs: tuple[str, ...] = ()

    def apply(self, txn: Txn, prior: tuple[Line, ...]) -> Decimal | None:
        fees = [line.amount for line in prior if line.kind == "fee"]
        return _bps(sum(fees), self.bps) if fees else None      # 没有费用行就没有税，不凑一行 0


@dataclass(frozen=True, slots=True)
class _Schedule:
    """一个商户的全部版本：两个等长、同下标的元组。不可变，发布时整体替换。"""

    starts: tuple[int, ...] = ()                  # 生效时间，严格升序
    versions: tuple[tuple[Rule, ...], ...] = ()   # 第 i 个版本的规则链（已排好执行顺序）


class FeeEngine:
    def __init__(self) -> None:
        self._schedules: dict[str, _Schedule] = {}
        self._publish_lock = threading.Lock()         # 只有发布需要锁；读路径只读不可变快照

    def publish(self, merchant: str, effective_from: int, rules: Sequence[Rule]) -> int:
        """为商户发布一个新版本，从 `effective_from` 起生效，返回版本号（从 1 开始）。

        生效时间必须严格晚于该商户上一个版本，否则 StaleVersion；规则集不合法抛 InvalidRuleSet。
        规则按 `needs` 做稳定的拓扑排序后存下（第 3 关），之后不可修改。
        """
        ordered = _in_dependency_order(rules)             # 先校验：失败时不改任何状态
        with self._publish_lock:
            old = self._schedules.get(merchant, _Schedule())
            if old.starts and effective_from <= old.starts[-1]:
                raise StaleVersion(f"{merchant}: 生效时间必须晚于 {old.starts[-1]}")
            self._schedules[merchant] = _Schedule(old.starts + (effective_from,), old.versions + (ordered,))
            return len(old.starts) + 1

    def quote(self, txn: Txn) -> tuple[Line, ...]:
        """按交易发生时生效的版本，依次运行规则，返回每一行。

        版本 = 最后一个生效时间不晚于 `txn.ts` 的版本（恰好等于生效时间属于新版本）；
        没有这样的版本抛 NoActiveRules。结果是 txn 和版本的纯函数，同样的输入永远得到同样的输出。
        """
        sched = self._schedules.get(txn.merchant, _Schedule())     # 一次读取，之后用的是同一份快照
        v = bisect_right(sched.starts, txn.ts)                     # 生效版本的个数，也就是版本号
        if v == 0:
            raise NoActiveRules(f"{txn.merchant} 在 {txn.ts} 没有生效的规则")
        return _run(sched.versions[v - 1], txn, v)

    # ---- 第 4 关（选做）：更正已发布的错误 -----------------------------------

    def reprice(self, txn: Txn, previous: Sequence[Line], rules: Sequence[Rule], version: int) -> tuple[Line, ...]:
        """用更正后的规则重算 `txn`，与当初的各行比较，只返回有差额的"调整行"。

        调整行的 kind 是 "adjustment"，金额 = 新金额 - 旧金额（按 rule_id 汇总），按 rule_id 排序，
        `version` 记在调整行上。旧各行不改：与账本一样，纠错只靠追加。
        """
        new = _totals(_run(_in_dependency_order(rules), txn, version))
        old = _totals(previous)
        return tuple(Line(rid, "adjustment", version, new.get(rid, 0) - old.get(rid, 0))
                     for rid in sorted(new.keys() | old.keys()) if new.get(rid, 0) != old.get(rid, 0))


def _run(rules: tuple[Rule, ...], txn: Txn, version: int) -> tuple[Line, ...]:
    lines: tuple[Line, ...] = ()
    for rule in rules:
        raw = rule.apply(txn, lines)
        if raw is not None:                               # None = 不适用，不产生这一行
            lines += (Line(rule.rule_id, rule.kind, version, _to_minor(raw)),)
    return lines


def _totals(lines: Sequence[Line]) -> dict[str, int]:
    out: dict[str, int] = {}
    for line in lines:
        out[line.rule_id] = out.get(line.rule_id, 0) + line.amount
    return out


# ---- 第 2 关：阶梯、封顶与保底 -------------------------------------------------


@dataclass(frozen=True, slots=True)
class Tiered:
    """分档累进费率：`tiers` 是 ((档上限, 费率bps), ...)，每一档只对落在这一档里的那部分金额收费，
    最后一档的上限必须是 None（不封顶）。例：((10000, 290), (None, 250)) 表示前 10000 收 2.9%，超出部分收 2.5%。
    各档先累加再取整一次，不是每档各取整。"""

    rule_id: str
    tiers: tuple[tuple[int | None, int], ...]
    fixed: int | Mapping[str, int] = 0
    kind: str = "fee"
    needs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        uppers = [u for u, _ in self.tiers]
        ok = (bool(uppers) and uppers[-1] is None
              and all(isinstance(u, int) for u in uppers[:-1])
              and all(a < b for a, b in zip(uppers[:-2], uppers[1:-1])))
        if not ok:
            raise InvalidRuleSet(f"{self.rule_id}: 阶梯上限必须严格递增，且最后一档为 None")

    def apply(self, txn: Txn, prior: tuple[Line, ...]) -> Decimal | None:
        if txn.amount <= 0:
            return None
        total, lower = Decimal(0), 0
        for upper, bps in self.tiers:
            top = txn.amount if upper is None else min(txn.amount, upper)
            if top > lower:
                total += _bps(top - lower, bps)
            if upper is None or txn.amount <= upper:
                break
            lower = upper
        return total + _fixed_for(self.fixed, txn.currency)


@dataclass(frozen=True, slots=True)
class Bounded:
    """装饰器：给任意规则加保底和封顶。不适用（None）的规则保持不适用，不会被保底硬凑出一行。"""

    rule_id: str
    inner: Rule
    minimum: int = 0
    maximum: int | None = None

    @property
    def kind(self) -> str:
        return self.inner.kind

    @property
    def needs(self) -> tuple[str, ...]:
        return self.inner.needs

    def apply(self, txn: Txn, prior: tuple[Line, ...]) -> Decimal | None:
        raw = self.inner.apply(txn, prior)
        if raw is None:
            return None
        raw = max(raw, Decimal(self.minimum))
        return raw if self.maximum is None else min(raw, Decimal(self.maximum))


# ---- 第 3 关：依赖顺序、按币种的固定费 ------------------------------------------


def _fixed_for(fixed: int | Mapping[str, int], currency: str) -> int:
    if isinstance(fixed, int):
        return fixed
    try:
        return fixed[currency]
    except KeyError:
        raise MissingCurrency(f"没有为 {currency} 配置固定费") from None


def _in_dependency_order(rules: Sequence[Rule]) -> tuple[Rule, ...]:
    """稳定的拓扑排序：能先跑的按原顺序先跑；ID 重复、依赖不存在、成环都抛 InvalidRuleSet。"""
    ids = [r.rule_id for r in rules]
    if len(set(ids)) != len(ids):
        raise InvalidRuleSet("规则 ID 重复")
    for r in rules:
        if missing := [n for n in r.needs if n not in ids]:
            raise InvalidRuleSet(f"{r.rule_id} 依赖不存在的规则 {missing}")
    pending, done, out = list(rules), set(), []
    while pending:
        ready = next((r for r in pending if all(n in done for n in r.needs)), None)
        if ready is None:                                 # 剩下的每条都在等别的剩下的：有环
            raise InvalidRuleSet(f"规则依赖成环: {[r.rule_id for r in pending]}")
        pending.remove(ready)
        done.add(ready.rule_id)
        out.append(ready)
    return tuple(out)
