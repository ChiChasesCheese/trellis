---
id: s06-money-integer-cents
node: stripe.money
type: qa
---

## Q
为什么金额题一定要转成整数最小单位（分）来算，浮点累加会在什么规模上出问题？如果必须用 `Decimal`，舍入模式要注意什么？零小数货币（JPY 等）怎么处理？

## A
**为什么考**：Stripe 的 API 本身就是整数最小单位（`amount: 1099` = $10.99）。
浮点累加的漂移会在第 1000 笔上显形，而 perf 测试正好用 10^5 条数据。

**铁律**（详见 `04-money-and-rounding.md`）：

1. **解析时立刻变成整数分**：`cents = int(round(Decimal(s) * 100))`，
   或者更安全：`d = Decimal(s); cents = int(d.scaleb(2))`（输入保证两位小数时）。
2. **中间计算全程用 `int`**。
3. **只在输出时格式化一次**：`f"{cents // 100}.{cents % 100:02d}"`，
   负数要单独处理符号，别指望 `//` 和 `%` 对负数的行为。
4. **零小数货币**（JPY、KRW、UGX 等）没有"分"，1 = 1 日元。题面给了货币列表就必须分开处理。

**如果必须用 `Decimal`**：显式给舍入模式，不要依赖默认：

```python
from decimal import Decimal, ROUND_HALF_UP
amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
```

Python 的 `round()` 是**banker's rounding**（四舍六入五成双）：`round(2.5) == 2`。
题面说 "round half up" 时用它就是错的。
