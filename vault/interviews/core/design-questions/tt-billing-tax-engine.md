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

**60 分钟路线。**

| 时间 | 做什么 |
|---|---|
| 0–8 分 | 问清需求，定接口：`publish`、`quote`，整数金额，取整规则 |
| 8–15 分 | 讲整体设计：版本按生效时间二分，规则链，税建在费用之上 |
| 15–45 分 | 写核心实现：`Txn`、`Line`、`Rule`、`PercentPlusFixed`、`TaxOnFees`、`FeeEngine` |
| 45–50 分 | 跑例子：352、44.5 取 44、版本边界、没有版本报错 |
| 50–60 分 | 追问：封顶装饰器、阶梯费率、错误规则补救、退款与多币种 |

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
- `Rule`（抽象类）：`apply(txn, prior_lines) -> Decimal | None`；`PercentPlusFixed`、`TaxOnFees` 是两个实现，`Capped` 见逐步扩展 1。
- `FeeEngine`：每个商户一对同下标的列表：生效时间 `starts` 和规则集 `versions`；`publish` 追加，`quote` 二分后运行规则链。
- 模式：策略（每条规则一种计算）、责任链（规则按顺序运行，后面的规则看得到前面的结果）、装饰器（`Capped` 包住任意规则）。

**整体设计。**
- `quote(txn)`：用 `txn.merchant` 取出该商户的 `starts` 列表，`bisect_right(starts, txn.ts)` 得到生效版本号（最后一个起始时间不晚于交易时间的版本），取这个版本的规则链依次运行。每条规则拿到交易和前面已经取整的各行，返回全精度的数值或「不适用」；引擎对返回值取整一次，生成 `Line` 追加到结果里。
- `publish`：要求生效时间严格大于该商户上一个版本的生效时间，`starts` 永远升序，二分才成立。想「修正历史定价」不是改旧版本，而是发布新版本，并对受影响的交易写调整行。发布时构造新列表再替换引用，读路径拿不可变数据，不需要锁。
- 「税在费用之上」不是特殊逻辑：`TaxOnFees` 是链上排在费用后面的一条规则，从 `prior` 里按 `kind == "fee"` 汇总。

**核心实现。** 82 行。

```python
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


class FeeEngine:
    def __init__(self) -> None:
        self._starts: dict[str, list[int]] = {}
        self._versions: dict[str, list[tuple[Rule, ...]]] = {}

    def publish(self, merchant: str, effective_from: int, rules: tuple[Rule, ...]) -> int:
        starts = self._starts.setdefault(merchant, [])
        if starts and effective_from <= starts[-1]:
            raise ValueError("版本只能向前追加")  # 历史靠新版本修正，不改旧版本
        starts.append(effective_from)
        self._versions.setdefault(merchant, []).append(rules)
        return len(starts)

    def quote(self, t: Txn) -> tuple[Line, ...]:
        v = bisect_right(self._starts.get(t.merchant, []), t.ts)  # 生效版本 = 最后一个 start <= ts
        if v == 0:
            raise LookupError(f"{t.merchant} 在 {t.ts} 没有生效的规则")  # 宁可报错，不返回 0
        lines: tuple[Line, ...] = ()
        for rule in self._versions[t.merchant][v - 1]:
            raw = rule.apply(t, lines)
            if raw is not None:
                lines += (Line(rule.rule_id, rule.kind, v, to_minor(raw)),)
        return lines
```

**运行。**

```python
e = FeeEngine()
e.publish("m1", 100, (PercentPlusFixed("fee", 290, 30), TaxOnFees("tax", 1000)))
e.publish("m1", 200, (PercentPlusFixed("fee", 250, 30), TaxOnFees("tax", 1000)))
```

- `ts = 150`、金额 10000 分：费用 `10000 × 2.9% + 30 = 320`，税 `320 × 10% = 32`，合计 352，版本都是 1。
- `ts = 150`、金额 500 分：费用精确值 44.5，银行家舍入到偶数得 44（四舍五入会得 45），税 4.4 取整为 4，合计 48。
- `ts = 199` 用版本 1，`ts = 200` 用版本 2（费用 280、税 28）：恰好等于生效时间属于新版本。
- `ts = 99`（早于所有版本）→ `LookupError`；发布生效时间不大于上一个版本 → `ValueError`。

**复杂度。** `quote` 是 `O(log V + R)`，`V` 是该商户的版本数，`R` 是规则数。

**逐步扩展。**
1. 【追问再讲】封顶与阶梯：新写一种规则，引擎不动。`Capped` 是装饰器，包住任何规则，把结果压到上限，规则 ID 和种类沿用被包的那条；阶梯费率是另一个实现，内部持有按金额区间排序的列表，用二分找档。

```python
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
```

发布 `(Capped("fee", PercentPlusFixed("pct", 290, 30), 500), TaxOnFees("tax", 1000))`：金额 10000 → 费用 320、税 32；金额 100000 → 费用压到 500、税 50。

**深入。**
1. 【必讲】为什么按生效时间二分，而不是「当前配置」。
   - 问题：规则会改。只保存当前配置，重算上个月的交易就会用今天的规则，账对不上；退款手续费复用了错误的价格计划是真实发生过的缺陷类型。
   - 选项：完整保存每个版本，按时间查；或只保存差异，查询时重放。差异方式省空间，但每次查询变慢且难以审计。
   - 选完整版本加二分：一个商户一年也就几十个版本，空间不是问题，换来任何一行费用都能凭「规则 ID + 版本号」精确复现。
   - 边界：交易时间恰好等于某个版本的生效时间，属于新版本（`bisect_right`），写一个测试固定这条约定。
2. 【必讲】取整：只在边界取整一次。
   - 问题：每个中间步骤都取整，误差累积；不同规则用不同的取整方式，同一笔交易换条路径结果就不同。
   - 做法：规则内部用 `Decimal` 全精度；引擎在每一行产出时调用唯一的 `to_minor` 取整一次。税规则看到的是已经取整的费用行，所以账面上每一行加起来就是总数。
   - 舍入方式：四舍五入在大量数据上让总额系统性偏高，银行家舍入（遇 0.5 取偶数）无偏。选哪个由合同或监管决定，关键是全系统只有一处实现。
   - 分摊：把一笔固定费分摊到多行时必须守恒，整数除法后把余数逐个分给前几行，而不是每行独立取整。
3. 【必讲】规则可组合：加一种规则不改引擎。
   - 规则有统一接口，引擎只负责顺序运行；阶梯、封顶、保底、按支付方式不同的费率都是新的规则对象。
   - 规则之间的依赖不是简单先后时（A 用 B 的结果、B 又用 C 的），发布时把规则建成有向无环图做拓扑排序，有环就拒绝发布。
   - 选规则对象加顺序链；依赖复杂时才引入图，过早引入会让简单场景难以理解。
4. 【追问再讲】没有生效版本就报错：返回 0 费用是静默漏收，有交易没收费，几个月后对账才发现。每一行都带规则 ID 和版本号，凭它们复现。
5. 【追问再讲】错误规则的补救：不改旧行。发布更正后的规则，对受影响的交易重新计算，差额 = 新结果 − 旧行，作为调整行追加。这与账本「只追加、用冲正修正」是同一个原则。多实例部署时，规则是带版本号的数据，每行记录用的版本，生效时间设在未来几分钟，让所有实例有时间拉取。
6. 【追问再讲】退款与多币种。
   - 退款的手续费按原交易所属的规则版本（或合同约定）计算，不是退款当天的规则；把「计算依据的时间」作为显式参数，不在引擎里读当前时间。
   - 多币种：固定费按币种配置，取整按该币种的小数位（日元 0 位，美元 2 位，科威特第纳尔 3 位）；跨币种换算放在引擎之外。

**取舍与追问。** 按被问到的可能性排，通常口述就够：
- 线程安全：读多写少，发布时用写锁或「复制后替换」，`quote` 只读不可变数据，不加锁。
- 如何测试：固定版本边界（等于生效时间）、取整临界值（x.5）、没有版本的报错、链顺序（税在费用后面）、同一输入重复调用结果相同、发布乱序被拒绝。

**级别期望。**
- 中级：写出按商户的规则、算出费用和税，用整数金额，没有规则时报错；核心实现能跑通例子。
- 高级：版本按生效时间二分，规则链可组合，取整只在边界一次，说清为什么不能用当前配置算历史交易。
- 资深/Staff：规则依赖图与拓扑排序、调整行与更正流程、多实例发布一致性、多币种与退款场景下的版本选择、审计与复现能力。

**先修概念。** [[hi-low-level-design-in-a-hurry-patterns|设计模式]]、[[hi-low-level-design-in-a-hurry-design-principles|设计原则]]、[[hi-low-level-design-in-a-hurry-oop-concepts|面向对象概念]]、[[hi-low-level-design-in-a-hurry-delivery|答题框架（Delivery Framework）]]、[[hi-system-design-core-concepts-data-modeling|数据建模]]

**同类题。** [[solution-amz-discount-engine|折扣引擎]]、[[solution-amz-aws-billing|云账单计费]]、[[tt-ai-assisted-order-validator|AI 辅助的订单校验规则（规则依赖图）]]、[[tt-currency-conversion-queries|汇率换算]]、[[05-payment-domain|支付领域知识]]
