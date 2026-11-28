---
id: hi-c-lld-parking-lot-b01-py-money-time
node: lld.problem-breakdowns.parking-lot.beyond
type: qa
step: 2
---
## Q
**停车场 · Python：整数向上取整与金额的精确计算**｜拓展 · 加分

`-(-a // b)` 为什么是向上取整？为什么不能直接 `math.ceil(a / b)`？

## A
**模式。** 整数分：金额与时长都用整数，全程不进入浮点。

```python
import math
from decimal import Decimal

HOUR = 3_600_000

assert 0.1 + 0.2 != 0.3                                  # 二进制浮点
assert Decimal("0.1") + Decimal("0.2") == Decimal("0.3") # 十进制小数类型是精确的


def hours_ceil(ms: int) -> int:
    return -(-ms // HOUR)           # // 向负无穷取整：-ms 向下取整后再取反，就是 ms 向上取整


assert [hours_ceil(x) for x in (0, 1, HOUR, HOUR + 1)] == [0, 1, 1, 2]

big = HOUR * 10**13 + 1             # 比 2^53 大得多：浮点放不下最后的 +1
assert hours_ceil(big) == 10**13 + 1
assert math.ceil(big / HOUR) == 10**13     # 浮点版本少算了一小时
```
- **底层：** Python 的 `int` 是任意精度，运算精确；`float` 只有 53 位有效数字，超过后相邻的整数无法区分，`/` 先转成浮点就已经丢了信息。
- **`Decimal` 的位置：** 需要保留小数的金额（税率、汇率）时用；这里的金额是整数分，不需要它。
- **另一种写法：** `(ms + HOUR - 1) // HOUR` 同样精确，对非负数更直观。
- **何时不用：** 展示用的近似值（比如"约 2.5 小时"）可以用浮点；进入计费的数据不行。
