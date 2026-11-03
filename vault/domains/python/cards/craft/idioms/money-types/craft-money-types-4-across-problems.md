---
id: craft-money-types-4-across-problems
node: craft.idioms.money-types
type: qa
step: 4
---
## Q
**金额类型 · 折扣、计费、外卖、打车的金额类型各是怎么落的**｜写法

五个系统都处理金额：折扣引擎、计费税引擎、外卖结算、打车车费、云计费。它们的类型选择有什么共同点，又在哪里分叉？

## A
**要点。** 共同点：入口一律不经过 `float`，存储一律是整数最小单位，取整点集中在一两处。分叉在**中间值**：折扣是整数运算；税和手续费要小数，用 `Decimal`；外卖要除以 60，用 `Fraction`；打车的倍数用 `Fraction`。

```python
# amz-discount-engine：字符串 -> 整数分，纯整数的四舍五入除法
def to_cents(text: str) -> int:
    return int((Decimal(text) * 100).quantize(Decimal(1), rounding=ROUND_HALF_UP))
def _div_half_up(numerator: int, denominator: int) -> int:
    return (2 * numerator + denominator) // (2 * denominator)

# billing-tax-engine：基点 x 金额，全精度 Decimal；取整只在一处
def _bps(amount: int | Decimal, bps: int) -> Decimal:
    return Decimal(amount) * bps / 10_000

# dasher-payout：费率 x 倍率 x 秒数 / 60，全程 Fraction
Fraction(self._plan.rates[state]) * Fraction(mult) * seconds / 60

# ride-sharing：涨价倍数在下单时锁死为 Fraction
surge: Fraction
return int((self.base + self.distance + self.time) * self.surge)
```

打车把倍数「锁死」在行程里，避免了对账差错：结算时倍数变了，同一趟行程会算出两个金额。云计费的 `Money` 值对象则在币种不同时抛错（见第 3 张卡）。证券的成交只在两个账户之间搬运整数分，不产生新钱。

**见于。** amz-discount-engine、billing-tax-engine、dasher-payout、ride-sharing、amz-aws-billing、stock-brokerage。

**信号。** 需求里有金额乘以百分比、倍数、按时间折算的费率；或者「分摊后总和要等于总额」。
