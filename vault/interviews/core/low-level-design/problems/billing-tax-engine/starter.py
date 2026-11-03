"""计费 / 计税引擎——起始模板。公开的类名、方法签名和异常与 solution.py 一致，把标了 NotImplementedError 的方法体补全。"""
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
    amount: int
    currency: str
    ts: int

@dataclass(frozen=True, slots=True)
class Line:
    rule_id: str
    kind: str
    version: int
    amount: int

class Rule(Protocol):
    """一条规则只需要会一件事：看交易和前面各行，给出全精度金额，或者"不适用"。结构化类型，不必继承。"""
    rule_id: str
    kind: str
    needs: tuple[str, ...]

    def apply(self, txn: Txn, prior: tuple[Line, ...]) -> Decimal | None:
        raise NotImplementedError

@dataclass(frozen=True, slots=True)
class PercentPlusFixed:
    """费用 = 金额 x 费率 + 固定费。`fixed` 可以是一个整数，或 {币种: 固定费}（第 3 关）。"""
    rule_id: str
    bps: int
    fixed: int | Mapping[str, int] = 0
    kind: str = 'fee'
    needs: tuple[str, ...] = ()

    def apply(self, txn: Txn, prior: tuple[Line, ...]) -> Decimal | None:
        """金额不是正数时不适用（返回 None）；固定费缺该币种时抛 MissingCurrency。"""
        raise NotImplementedError

@dataclass(frozen=True, slots=True)
class TaxOnFees:
    """税 = 前面各行里 kind 为 "fee" 的金额合计 x 税率。税看到的是已经取整的费用行，账面上每行相加就是总数。"""
    rule_id: str
    bps: int
    kind: str = 'tax'
    needs: tuple[str, ...] = ()

    def apply(self, txn: Txn, prior: tuple[Line, ...]) -> Decimal | None:
        raise NotImplementedError

class FeeEngine:

    def __init__(self) -> None:
        raise NotImplementedError

    def publish(self, merchant: str, effective_from: int, rules: Sequence[Rule]) -> int:
        """为商户发布一个新版本，从 `effective_from` 起生效，返回版本号（从 1 开始）。

生效时间必须严格晚于该商户上一个版本，否则 StaleVersion；规则集不合法抛 InvalidRuleSet。
规则按 `needs` 做稳定的拓扑排序后存下（第 3 关），之后不可修改。"""
        raise NotImplementedError

    def quote(self, txn: Txn) -> tuple[Line, ...]:
        """按交易发生时生效的版本，依次运行规则，返回每一行。

版本 = 最后一个生效时间不晚于 `txn.ts` 的版本（恰好等于生效时间属于新版本）；
没有这样的版本抛 NoActiveRules。结果是 txn 和版本的纯函数，同样的输入永远得到同样的输出。"""
        raise NotImplementedError

    def reprice(self, txn: Txn, previous: Sequence[Line], rules: Sequence[Rule], version: int) -> tuple[Line, ...]:
        """用更正后的规则重算 `txn`，与当初的各行比较，只返回有差额的"调整行"。

调整行的 kind 是 "adjustment"，金额 = 新金额 - 旧金额（按 rule_id 汇总），按 rule_id 排序，
`version` 记在调整行上。旧各行不改：与账本一样，纠错只靠追加。"""
        raise NotImplementedError

@dataclass(frozen=True, slots=True)
class Tiered:
    """分档累进费率：`tiers` 是 ((档上限, 费率bps), ...)，每一档只对落在这一档里的那部分金额收费，
    最后一档的上限必须是 None（不封顶）。例：((10000, 290), (None, 250)) 表示前 10000 收 2.9%，超出部分收 2.5%。
    各档先累加再取整一次，不是每档各取整。"""
    rule_id: str
    tiers: tuple[tuple[int | None, int], ...]
    fixed: int | Mapping[str, int] = 0
    kind: str = 'fee'
    needs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        raise NotImplementedError

    def apply(self, txn: Txn, prior: tuple[Line, ...]) -> Decimal | None:
        raise NotImplementedError

@dataclass(frozen=True, slots=True)
class Bounded:
    """装饰器：给任意规则加保底和封顶。不适用（None）的规则保持不适用，不会被保底硬凑出一行。"""
    rule_id: str
    inner: Rule
    minimum: int = 0
    maximum: int | None = None

    @property
    def kind(self) -> str:
        raise NotImplementedError

    @property
    def needs(self) -> tuple[str, ...]:
        raise NotImplementedError

    def apply(self, txn: Txn, prior: tuple[Line, ...]) -> Decimal | None:
        raise NotImplementedError
