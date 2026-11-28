---
id: py-out-numbers-round-bankers
node: output.numbers
type: qa
step: 2
---
## Q
**round 的银行家舍入**｜读代码说输出

```python
print(round(0.5), round(1.5), round(2.5))
print(round(2.675, 2), round(-0.5))
```

输出什么？

## A
**输出。**
```
0 2 2
2.67 0
```

**为什么。**
- Python 3 的 `round` 对恰好在中间的数取最近的偶数（银行家舍入，round half to even）：0.5 到 0，1.5 和 2.5 都到 2。
- `round(2.675, 2)` 得 2.67 不是 2.68：2.675 在二进制浮点里实际略小于 2.675，并不是恰好在中间。
- `round(-0.5)` 得 0（整数，不带负号）。

**语言为什么这样设计。**
- 偶数舍入让大量数据求和时舍入误差正负抵消，不会像“四舍五入”那样系统性偏大；IEEE 754 的默认舍入模式也是它。Python 2 是四舍五入，3.0 改了。
- Java 的 `Math.round` 与 JavaScript 的 `Math.round` 都是向正无穷方向“半入”，Java 的 `BigDecimal` 则要显式选 `RoundingMode`。

**怎么写才对。**
```python
from decimal import Decimal, ROUND_HALF_UP
Decimal("2.675").quantize(Decimal("0.01"), ROUND_HALF_UP)   # 钱用 Decimal
```

**面试里一句话。**
Python 3's `round` rounds ties to the nearest even number, and the float itself may not be an exact tie, so use `Decimal` when money needs half-up.
