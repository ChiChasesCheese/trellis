---
id: craft-round-once-at-the-boundary-5-across-problems
node: craft.idioms.round-once-at-the-boundary
type: qa
step: 5
---
## Q
**在边界处取整一次 · 计费、外卖、折扣、停车里取整点的位置**｜写法

计费税引擎、外卖结算、折扣引擎、停车费系统和分账都要把精确的中间值落成整数分。它们的取整点放在哪里，彼此怎么不同？

## A
**要点。** 同一个原则：取整只发生在「产出一个对外可见的金额」的那一刻，之前全精度。不同的是**这一刻是什么**：一行账单、一张订单、一个日历日、一次分账。

```python
# billing-tax-engine：全系统唯一取整点，一行只取整一次
def _to_minor(x: Decimal) -> int:
    return int(x.quantize(Decimal(1), rounding=ROUND_HALF_EVEN))

# dasher-payout：每单最后做一次（0.5 进位），分段金额一路是 Fraction
def _cents(x: Fraction) -> Decimal:
    return Decimal(int(x * 100 + Fraction(1, 2))).scaleb(-2)

# amz-parking-fees：每个日历日取整一次（向上），再套当天封顶
raw = Money(-(-units[day] // 3600))
result.append(DayCharge(day, seconds[day], raw, min(raw, cap)))

# splitwise：向下取整后按小数部分大小补回损失的最小单位
floors = {u: exact[u].numerator // exact[u].denominator for u in order}
remainder = amount - sum(floors.values())
```

停车费的取整点放在「每天」是业务要求：封顶按日算，必须先得到当天的整数分，才能和封顶比较。取整点的选择先于舍入模式的选择：先问「哪个金额是对外承诺的单位」，再问怎么舍。

**见于。** billing-tax-engine、dasher-payout、amz-discount-engine、amz-parking-fees、splitwise。

**信号。** 代码里同一个金额经过多步计算，并且有 `round`、`int()`、`quantize`、`//` 出现在中间步骤；或者「各行之和与总额差几分」的 bug 报告。
