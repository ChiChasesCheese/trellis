---
id: pay-platform-subscriptions-proration
node: platform.subscriptions
type: qa
step: 4
---
## Q
用户在账期中途升级套餐，按比例计费（proration）怎么算？请写出带舍入的实现并解释结果。

## A
**场景**：用户月付 10.00 美元的基础版，账期共 30 天，第 10 天升级到 30.00 美元的高级版，当前账期还剩 20 天。

**算法**
1. 退还旧计划未用部分的额度（credit）：10.00 × 20/30。
2. 按新计划收取剩余天数的费用（charge）：30.00 × 20/30。
3. 本次应补差额 = 收费 − 额度。

```python
from decimal import Decimal, ROUND_HALF_EVEN

def prorate(old: int, new: int, days_left: int, days: int) -> tuple[int, int, int]:
    f = Decimal(days_left) / Decimal(days)
    r = lambda x: int((Decimal(x) * f).quantize(Decimal(1), ROUND_HALF_EVEN))
    credit, charge = r(old), r(new)
    return credit, charge, charge - credit

print(prorate(1000, 3000, 20, 30))
print(prorate(1000, 3000, 21, 31))
```
实际输出：
```
(667, 2000, 1333)
(677, 2032, 1355)
```
第一行：额度 6.67 美元，新计划费用 20.00 美元，补差额 13.33 美元。第二行是 31 天的账期、剩余 21 天的情形：额度 6.77，收费 20.32，补差额 13.55。

**要点**
1. 金额用最小货币单位整数，只在最后舍入，且先分别舍入额度和费用，再相减，保证账单上每一行明细加起来等于总额。
2. 比例的天数口径（按日历天数还是按秒）要统一，并写进计费规则。
3. 降级时通常不立即退款，而是在账期末生效，或把差额作为账户余额抵扣下期。
4. 账单上展示每一行（旧计划未用额度、新计划费用），用户才能看懂金额，减少拒付。
