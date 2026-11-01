---
slug: tt-billing-tax-engine
kind: low-level-design
---
## Q
**计费 / 计税引擎**｜低层设计

设计一个计费与计税引擎：每个商户配置自己的费用规则（例如"2.9% 加 0.30"），税在费用之上再算（例如费用的 10%）；`quote(txn)` 返回这笔交易的每一行费用，每行带规则 ID、规则版本和金额。商户的规则会改，新规则从某个时间点起生效，历史交易必须按交易发生时生效的规则计算，之后重算也要得到完全一样的数字。面试官会一条一条往上加需求：阶梯费率、封顶与保底、多币种、规则之间的依赖、发布了错误规则后怎么补救、多实例部署下规则怎么更新。

给出完整解答：需求、核心实体与接口、整体设计、深入问题、取舍、不同级别的期望。

## A
**一句话。** 这是"带生效时间的版本化规则 + 可组合的规则链 + 金额只在边界取整一次"的组合：每个商户的规则版本按生效时间排序后二分查找，规则本身是可调用对象排成链，使得加一种费用或一种税不用改引擎，并且任何一行金额都能被复现。

**需求。**
功能：
1. `publish(merchant, effective_from, rules)`：为商户发布一个新版本的规则集，从某个时间点起生效。
2. `quote(txn)`：按交易发生的时间找到当时生效的版本，依次运行规则，返回每一行（规则 ID、种类、版本、金额）。
3. 税规则能引用前面的费用行（税算在费用之上）。
4. 没有生效版本时明确报错。
5. 加一种新规则（阶梯、封顶、保底）不修改引擎。

非功能：
- 金额是整数最小货币单位；规则内部用 `Decimal` 全精度，**每一行只取整一次**，取整方式（银行家舍入）全系统一致。
- 同一笔交易、同一个版本，结果永远相同（纯函数，无隐藏状态、不读当前时间）。
- 查询 O(log V)，V 为该商户的版本数；读多写少，读路径不加锁。

**核心实体与接口。**
- `Txn(id, merchant, amount, currency, ts)`：不可变，`ts` 是交易发生时间。
- `Line(rule_id, kind, version, amount)`：费用的一行，`kind` 区分费用与税，让税规则按种类汇总。
- `Rule`（抽象类）：`apply(txn, prior_lines) -> Decimal | None`；`PercentPlusFixed`、`TaxOnFees`、`Capped` 是三个实现。
- `FeeEngine`：每个商户一对同下标的列表：生效时间 `starts` 和规则集 `versions`；`publish` 追加，`quote` 二分后运行规则链。
- 模式：策略（每条规则一种计算）、责任链（规则按顺序运行，后面的规则看得到前面的结果）、装饰器（`Capped` 包住任意规则）。

```python
from __future__ import annotations

from abc import ABC, abstractmethod
from bisect import bisect_right
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_EVEN


@dataclass(frozen=True)
class Txn:
    id: str
    merchant: str
    amount: int          # 最小货币单位（分）
    currency: str
    ts: int              # 交易发生时间，epoch 秒；永远不用"处理时间"


@dataclass(frozen=True)
class Line:
    rule_id: str
    kind: str            # "fee" 或 "tax"：税规则按 kind 汇总，不靠名字猜
    version: int
    amount: int          # 整数分


def to_minor(x: Decimal) -> int:
    """全系统唯一的取整点：银行家舍入，一行只取整一次。"""
    return int(x.quantize(Decimal(1), rounding=ROUND_HALF_EVEN))


class Rule(ABC):
    rule_id: str
    kind: str

    @abstractmethod
    def apply(self, t: Txn, prior: tuple[Line, ...]) -> Decimal | None:
        """返回全精度的费用（None 表示不适用）；prior 是链上前面已经取整的各行。"""


@dataclass(frozen=True)
class PercentPlusFixed(Rule):
    rule_id: str
    bps: int             # 290 = 2.9%
    fixed: int           # 固定费，分
    kind: str = "fee"

    def apply(self, t, prior):
        return Decimal(t.amount) * self.bps / 10_000 + self.fixed if t.amount > 0 else None


@dataclass(frozen=True)
class TaxOnFees(Rule):
    rule_id: str
    bps: int
    kind: str = "tax"

    def apply(self, t, prior):
        fees = sum(l.amount for l in prior if l.kind == "fee")
        return Decimal(fees) * self.bps / 10_000


@dataclass(frozen=True)
class Capped(Rule):
    """装饰器：给任意规则加封顶。"""
    rule_id: str
    inner: Rule
    cap: int

    @property
    def kind(self) -> str:
        return self.inner.kind

    def apply(self, t, prior):
        v = self.inner.apply(t, prior)
        return None if v is None else min(v, Decimal(self.cap))


class FeeEngine:
    def __init__(self) -> None:
        self._starts: dict[str, list[int]] = {}
        self._versions: dict[str, list[tuple[Rule, ...]]] = {}

    def publish(self, merchant: str, effective_from: int, rules: tuple[Rule, ...]) -> int:
        starts = self._starts.setdefault(merchant, [])
        if starts and effective_from <= starts[-1]:
            raise ValueError("版本只能向前追加")          # 历史靠新版本修正，不改旧版本
        starts.append(effective_from)
        self._versions.setdefault(merchant, []).append(rules)
        return len(starts)

    def quote(self, t: Txn) -> tuple[Line, ...]:
        v = bisect_right(self._starts.get(t.merchant, []), t.ts)    # 生效版本 = 最后一个 start <= ts
        if v == 0:
            raise LookupError(f"{t.merchant} 在 {t.ts} 没有生效的规则")  # 宁可报错，不返回 0
        lines: tuple[Line, ...] = ()
        for rule in self._versions[t.merchant][v - 1]:
            raw = rule.apply(t, lines)
            if raw is not None:
                lines += (Line(rule.rule_id, rule.kind, v, to_minor(raw)),)
        return lines
```

测试数字：金额 10000 分（100.00 美元），费率 2.9% 加 30 分，费用 = 290 + 30 = 320 分，税 = 320 的 10% = 32 分，合计 352。金额 500 分时费用精确值是 44.5 分，银行家舍入到最近的偶数得 44（四舍五入会得 45），税 4.4 分取整为 4。这个例子说明取整规则必须写进规范，而不是留给调用方。

**整体设计。**
调用路径：`quote(txn)` → 用 `txn.merchant` 取出该商户的 `starts` 列表 → `bisect_right(starts, txn.ts)` 得到生效版本号（最后一个起始时间不晚于交易时间的版本）→ 取这个版本的规则链 → 依次运行：每条规则拿到交易和前面已经取整的各行，返回全精度的数值或"不适用"→ 引擎对返回值取整一次，生成 `Line` 追加到结果里。

发布路径：`publish` 要求生效时间严格大于该商户上一个版本的生效时间，因此 `starts` 永远是升序的，二分才成立。想"修正历史定价"不是改旧版本，而是发布新版本并对受影响的交易写调整行。

规则链里"税在费用之上"并不是特殊逻辑：`TaxOnFees` 是链上排在费用后面的一条规则，它从 `prior` 里按 `kind == "fee"` 汇总。要让税也被另一个税二次征收，只需把汇总条件改一改。

**深入。**

1. 为什么按生效时间二分，而不是"当前配置"。
- 问题：规则会改。如果引擎只保存当前配置，那么重新计算上个月的交易就会用今天的规则，账对不上；更糟的是退款手续费复用了错误的价格计划，这是真实发生过的缺陷类型。
- 选项：把每个版本的完整规则集都保留，按时间查；或者只保存差异，查询时重放。完整保存最简单，查询是一次二分；差异方式省空间但让每次查询变慢而且难以审计。
- 选择：完整版本加二分。版本数很小（一个商户一年也就几十次修改），空间不是问题，换来的是任何一行费用都能凭"规则 ID + 版本号"精确复现。
- 边界：交易时间恰好等于某个版本的生效时间时，属于新版本（`bisect_right`）；一定要写一个测试固定这条约定。

2. 取整：只在边界取整一次。
- 问题：如果每个中间步骤都取整，误差会累积；如果不同规则用不同的取整方式，同一笔交易换条路径结果就不同。
- 做法：规则内部用 `Decimal` 保持全精度；引擎在每一行产出时调用唯一的 `to_minor` 取整一次。税规则看到的是已经取整的费用行，因此"费用 + 税"的每一行加起来就是账面上的数，不会出现展示的金额与计算的金额差一分。
- 选项：四舍五入（0.5 总是进位）在大量数据上会让总额系统性偏高；银行家舍入（遇到 0.5 取偶数）无偏。选哪一个由合同或监管决定，关键是全系统只有一处实现。
- 分摊：如果要把一笔固定费分摊到多行，必须守恒（各行之和等于总数），做法是整数除法后把余数逐个分给前几行，而不是每行独立取整。

3. 规则可组合：加一种规则不改引擎。
- 问题：业务会不断提出阶梯费率（交易量越大费率越低）、封顶、保底、按支付方式不同的费率。
- 做法：规则是一个有统一接口的对象，引擎只负责顺序运行。`Capped` 展示了装饰器：它包住任何规则，把结果压到上限，规则 ID 和种类沿用被包的那条。阶梯费率是另一个实现，内部持有一个按金额区间排序的列表，同样用二分查找适用的档。
- 依赖：如果规则之间的依赖不是简单的先后顺序（比如 A 要用 B 的结果、B 又要用 C 的），发布时把规则建成有向无环图做一次拓扑排序，得到链的顺序，有环就拒绝发布。这与编码题里"规则依赖图上删除一个节点并重连前后节点"是同一个结构。
- 选择：规则对象 + 顺序链；依赖复杂时才引入图。过早引入图会让简单场景难以理解。

4. 不变量与失败方式。
- 每一行都带规则 ID 和版本号，凭它们可以复现。
- 没有生效版本时抛错，而不是返回 0 费用。返回 0 的后果是"有交易、没收费"的静默漏收，要几个月后对账才发现。
- 版本只追加：发布新版本不影响已经算出的行；读路径拿到的是不可变的元组，发布时构造新列表再替换引用，读路径不需要锁。

**取舍与追问。**
- 加阶梯费率、封顶和保底？新写一种规则；封顶和保底是包在另一条规则外面的装饰器，引擎不动。
- 多币种？交易带币种，固定费按币种配置；取整按该币种的小数位（日元 0 位，美元 2 位，科威特第纳尔 3 位）；跨币种的换算放在引擎之外，引擎只接受已经统一币种的金额。
- 发布了错误的规则，已经算出的费用怎么办？不改旧行。发布更正后的规则，再对受影响的交易重新计算，差额 = 新结果 − 旧行，作为"调整行"追加。这与账本的"只追加、用冲正修正"是同一个原则。
- 规则热更新，多个实例如何保持一致？规则是带版本号的数据，实例按版本号拉取；每行费用记录用的版本号，所以即使两个实例短暂不同步，也能事后精确核对哪一笔用了哪个版本。生效时间设在未来几分钟，让所有实例有时间拉取。
- 线程安全？读多写少，发布时用写锁或"复制后替换"，`quote` 只读不可变数据，不加锁。
- 费用要按事件发生时的规则算，退款呢？退款的手续费要按原交易所属的规则版本（或合同约定的规则）计算，而不是退款当天的规则；把"计算依据的时间"作为显式参数，而不是在引擎里读当前时间。
- 如何测试？固定版本边界（等于生效时间）、取整的临界值（x.5）、没有版本的报错、链顺序（税在费用后面）、同一输入重复调用结果相同、发布乱序被拒绝。

**级别期望。**
- 中级：写出按商户的规则、算出费用和税，用整数金额，没有规则时报错。
- 高级：版本按生效时间二分，规则链可组合，取整只在边界一次，说清为什么不能用当前配置算历史交易。
- 资深/Staff：规则依赖图与拓扑排序、调整行与更正流程、多实例发布一致性、多币种与退款场景下的版本选择、审计与复现能力。

**先修概念。** [[hi-low-level-design-in-a-hurry-patterns|设计模式]]、[[hi-low-level-design-in-a-hurry-design-principles|设计原则]]、[[hi-low-level-design-in-a-hurry-oop-concepts|面向对象概念]]、[[hi-low-level-design-in-a-hurry-delivery|答题框架（Delivery Framework）]]、[[hi-system-design-core-concepts-data-modeling|数据建模]]

**同类题。** [[solution-amz-discount-engine|折扣引擎]]、[[solution-amz-aws-billing|云账单计费]]、[[tt-ai-assisted-order-validator|AI 辅助的订单校验规则（规则依赖图）]]、[[tt-currency-conversion-queries|汇率换算]]、[[05-payment-domain|支付领域知识]]
