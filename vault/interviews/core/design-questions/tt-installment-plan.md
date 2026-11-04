---
slug: tt-installment-plan
kind: low-level-design
---
## Q
**分期计划生成器**｜低层设计

设计并实现分期还款计划的生成器（先买后付、消费分期会用到）：输入本金（最小货币单位，例如分）、期数、年化利率（用基点，1200 表示 12%）和起始日期，输出每一期的到期日、本金和利息。利率为 0 时是免息分期（例如分 4 期、每两周一期）。面试官会往上加需求：提前还款、逾期与逾期费、一笔还款怎么分配到各期、按日计息、到期日遇到节假日、等额本金与等额本息两种算法。重点考察金额取整、分摊后总和守恒、日期的月末处理。

给出完整解答：需求、核心实体与接口、整体设计、深入问题、取舍、不同级别的期望。

## A
**一句话。** 这是一个纯函数问题：难点不在算法而在三个细节——各期本金之和必须恰好等于本金（取整误差只能由最后一期吸收），到期日要从起始日一次性算出而不是逐期累加，金额全程用整数和定点小数而不用浮点。

**60 分钟路线。**

| 时间 | 做什么 |
|---|---|
| 0–8 分 | 问清需求，定接口：`schedule(principal, n, apr_bps, start, step)`，整数金额 |
| 8–15 分 | 讲整体设计：先算到期日，免息均分，有息等额本息，最后一期吸收误差 |
| 15–45 分 | 写核心实现：`Instalment`、`add_months`、`split_evenly`、`schedule` |
| 45–50 分 | 跑例子：120000 分 12 期，免息 10001 分 4 期 |
| 50–60 分 | 追问：等额本金、提前还款、逾期、按日计息 |

**需求。**
功能：
1. **schedule 返回不可变计划：** `schedule(principal, n, apr_bps, start, step)` 返回不可变的还款计划：每期序号、到期日、本金、利息。
2. 有息时采用等额本息：每期还款额相同，最后一期吸收取整误差。
3. 免息时把本金尽量均分，余数分给前几期。
4. 到期日按月或按两周推进，月末日期按当月天数截断。
5. **非法输入报错：** 非法输入（本金、期数不为正，利率为负）报错。

非功能：
- 金额是整数最小货币单位；中间计算用 `Decimal`，每个金额只取整一次（银行家舍入）。
- 纯函数：不读当前时间，不修改入参，同样输入永远得到同样输出，便于测试和审计。
- 时间复杂度 O(n)。

**核心实体与接口。**
- **Instalment 是一期：** `Instalment(seq, due, principal, interest)`：一期，`total` 属性是本息合计；不可变。
- `schedule(...)`：生成计划，返回 `Instalment` 的元组。
- `step`：到期日策略函数（`monthly`、`biweekly`），决定「第 k 期的到期日」，通过参数注入，加新节奏不改主函数。例如 pay-in-4：`biweekly` 作 `step`，利率传 0。
- `split_evenly(total, n)`：守恒分摊的工具函数。
- 模式：无状态的纯函数加策略参数；值对象不可变。

**整体设计。** `schedule` 的流程：
1. 校验输入。
2. 先算出全部到期日：第 i 期是 `step(start, i)`，每次都从起始日出发，而不是在上一期日期上加一个周期。
3. 利率为 0：`split_evenly` 一次算出各期本金，利息全部为 0。
4. 利率大于 0：月利率 `r = apr_bps / 10000 / 12`，等额本息的每期还款额是 `P × r / (1 − (1 + r)^−n)`，取整一次。逐期循环：利息 = 剩余本金 × r（取整一次）；本金 = 每期还款额 − 利息；最后一期的本金直接取剩余本金，让余额恰好归零。
5. 返回不可变的元组。

**核心实现。** 63 行。

```python
import calendar
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_EVEN
from typing import Callable


@dataclass(frozen=True)
class Instalment:
    seq: int
    due: date
    principal: int           # 最小货币单位
    interest: int

    @property
    def total(self) -> int:
        return self.principal + self.interest


def add_months(d: date, k: int) -> date:
    """从起始日加 k 个月，月末截断：1 月 31 日 + 1 个月 = 2 月 28/29 日。"""
    y, m = divmod(d.month - 1 + k, 12)
    year, month = d.year + y, m + 1
    return date(year, month, min(d.day, calendar.monthrange(year, month)[1]))


def monthly(start: date, k: int) -> date:
    return add_months(start, k)


def biweekly(start: date, k: int) -> date:
    return start + timedelta(days=14 * k)


def split_evenly(total: int, n: int) -> list[int]:
    """分摊守恒：整数除法，余数逐个分给前几期，合计恰好等于 total。"""
    base, extra = divmod(total, n)
    return [base + (1 if i < extra else 0) for i in range(n)]


def to_minor(x: Decimal) -> int:
    return int(x.quantize(Decimal(1), rounding=ROUND_HALF_EVEN))


def schedule(principal: int, n: int, apr_bps: int, start: date,
             step: Callable[[date, int], date] = monthly) -> tuple[Instalment, ...]:
    """纯函数：同样的输入永远得到同样的计划。apr_bps=1200 表示年化 12%。"""
    if principal <= 0 or n <= 0 or apr_bps < 0:
        raise ValueError("本金、期数必须为正，利率不能为负")
    due = [step(start, i + 1) for i in range(n)]            # 每次都从起始日算，不累加，避免漂移
    if apr_bps == 0:                                         # 免息分期（如 pay-in-4）
        parts = split_evenly(principal, n)
        return tuple(Instalment(i + 1, due[i], parts[i], 0) for i in range(n))
    r = Decimal(apr_bps) / 10_000 / 12                       # 月利率
    pay = to_minor(principal * r / (1 - (1 + r) ** -n))      # 等额本息的每期还款额
    out: list[Instalment] = []
    bal = principal
    for i in range(n):
        interest = to_minor(bal * r)                         # 利息按剩余本金逐期算
        p = bal if i == n - 1 else pay - interest            # 最后一期吸收全部取整误差
        out.append(Instalment(i + 1, due[i], p, interest))
        bal -= p
    return tuple(out)
```

**运行。**

```python
plan = schedule(120000, 12, 1200, date(2026, 1, 31))   # 1,200.00，12 期，年化 12%
```

- 每期还款额 10662 分。第 1 期到期日 2026-02-28（1 月 31 日加一个月，截断到 2 月底），利息 1200、本金 9462；第 2 期 2026-03-31，利息 1105、本金 9557。
- **末期吸收取整误差：** 最后一期（2027-01-31）本金 10554、利息 106，合计 10660，比其他期少 2 分，因为它吸收了前面各期的取整误差。
- 全部本金之和恰好是 120000，总利息 7942。
- **示例：本金拆成 2501、2500：** `schedule(10001, 4, 0, date(2026, 1, 1), biweekly)` → 本金 2501、2500、2500、2500，到期日 1 月 15 日、1 月 29 日、2 月 12 日、2 月 26 日。
- 本金、期数不为正或利率为负 → `ValueError`。

**复杂度。** 时间和空间都是 `O(n)`。

**逐步扩展。**
1. 【追问再讲】等额本金：每期本金相同（守恒分摊），利息仍按剩余本金逐期算。只是把「每期还款额」换成「每期本金」，共用日期和取整工具。

```python
def schedule_equal_principal(principal: int, n: int, apr_bps: int, start: date,
                             step: Callable[[date, int], date] = monthly) -> tuple[Instalment, ...]:
    if principal <= 0 or n <= 0 or apr_bps < 0:
        raise ValueError("本金、期数必须为正，利率不能为负")
    r = Decimal(apr_bps) / 10_000 / 12
    parts = split_evenly(principal, n)  # 每期本金守恒分摊
    out, bal = [], principal
    for i in range(n):
        out.append(Instalment(i + 1, step(start, i + 1), parts[i], to_minor(bal * r)))
        bal -= parts[i]
    return tuple(out)
```

同一笔 120000 分、12 期、月利率 1%：总利息 7800（等额本息是 7942），前三期合计 11200、11100、11000，最后一期 10100，本金之和仍是 120000。

**深入。**
1. 【必讲】金额与取整：为什么用整数加 `Decimal`。
   - 问题：浮点数 `0.1 + 0.2` 不等于 `0.3`，上千万笔之后误差变成对不上的账。
   - 做法：本金和每个结果都是整数最小货币单位；中间的公式用 `Decimal` 全精度；每个输出金额在产出时取整一次。
   - 舍入：银行家舍入在大量数据上无偏，四舍五入会让总额系统性偏高。具体用哪个由合同和监管决定，关键是只有一处实现。
   - 币种：最小单位由调用方按币种小数位换算（日元 0 位，美元 2 位，科威特第纳尔 3 位），函数本身不关心。
2. 【必讲】守恒：各期之和必须等于本金。
   - 问题：把 10000 分分 3 期，每期独立四舍五入得到 3333 × 3 = 9999，少了 1 分。
   - 免息：`divmod(10000, 3)` 得 3333 余 1，余数给第 1 期，得 3334、3333、3333，合计 10000。余数给前几期还是最后一期要写进规范并固定。
   - 有息：每期还款额取整后与精确值有差异，利息又各自取整，误差逐期累积到剩余本金里。让最后一期的本金等于剩余本金，总本金就不差一分；代价是最后一期的合计金额可能比其他期多或少几分，合同里要明确声明。
   - 不变量：各期本金之和等于本金；到期日严格递增；没有负数金额；最后一期结束时剩余本金为 0。
3. 【必讲】日期：月末与不漂移。
   - 问题：用「上一期加一个月」，1 月 31 日起算会变成 2 月 28 日，再加一个月变成 3 月 28 日，永远回不到 31 日。
   - 做法：每期都是「起始日加 k 个月」，月末截断（`min(day, 当月天数)`）：2 月 28 日、3 月 31 日、4 月 30 日。
   - 两周一期：起始日加 14 × k 天，天然不涉及月末。
   - 节假日：合同到期日保存在计划里，实际扣款日（遇非工作日顺延）另外存，计划本身保持纯函数。
4. 【追问再讲】等额本息与等额本金：等额本息每期还款额相同，易预算，前期利息多本金少；等额本金每期本金相同，前期还款多、逐期递减，总利息更少。消费金融以等额本息为主；面试时先实现一种，说清另一种怎么换（逐步扩展 1）。
5. **【追问再讲】提前还款与逾期：** 提前还款、逾期与还款分配（见取舍与追问）。
6. 【加分】计划不可变与按日计息。
   - 计划是合同的一部分，必须可追溯；提前还款、展期都生成新计划并保留旧计划，纠纷时能还原每一刻的状态。
   - 按日计息：每期利息 = 剩余本金 × 年化利率 ÷ 365 × 当期天数，各期天数不同，所以每期还款额不再相等；最后一期仍然吸收误差。

**取舍与追问。** 按被问到的可能性排，通常口述就够：
- 提前还款：用剩余本金和剩余期数重新调用同一个函数生成新计划，旧计划标记为被替代，不删除；提前还款当期的利息按实际天数结算。
- 逾期：计划之外另设还款记录表；逾期天数 = 今天 − 最早一期未还清的到期日，按 1 到 30、31 到 60、61 到 90、90 天以上分桶；逾期费是一条新的费用行，不改计划。
- 一笔还款怎么分配：按固定顺序冲抵，常见是费用、利息、本金，从最早一期开始；顺序由合同和监管决定，做成配置而不是写死的分支，并可审计。
- 如何测试：利率为 0 的守恒（含余数）、月末起算（1 月 31 日、闰年 2 月 29 日）、期数为 1、极小本金小于期数、最后一期余额归零、输入非法。

**级别期望。**
- 中级：写出等额本息公式，生成每期的本金与利息，用整数金额；核心实现能跑通例子。
- 高级：守恒分摊与最后一期吸收误差，起始日加 k 个月不漂移，策略注入日期规则，纯函数与不可变对象。
- 资深/Staff：提前还款与重排计划、逾期分桶与还款分配顺序、按日计息、计划版本化与审计、与账本和授信模块的接口。

**先修概念。** [[hi-low-level-design-in-a-hurry-design-principles|设计原则]]、[[hi-low-level-design-in-a-hurry-oop-concepts|面向对象概念]]、[[hi-low-level-design-in-a-hurry-patterns|设计模式]]、[[hi-low-level-design-in-a-hurry-delivery|答题框架（Delivery Framework）]]

**同类题。** [[tt-currency-conversion-queries|汇率换算]]、[[tt-billing-tax-engine|计费 / 计税引擎]]、[[tt-double-entry-ledger|复式账本（类设计）]]、[[solution-amz-parking-fees|停车费计算]]、[[05-payment-domain|支付领域知识]]
