---
id: tlc-python-pitfalls-5-float-int
node: python.pitfalls
type: qa
step: 5
---
## Q
**Python 陷阱｜浮点比较、`round` 和取整方向**

为什么不能用 `==` 比较浮点数？`round(2.5)` 是多少？除法取整的方向在负数上有什么坑？

## A
浮点数用二进制近似小数，`0.1`、`0.2` 都不能精确表示。

```python
import math
print(0.1 + 0.2, 0.1 + 0.2 == 0.3)               # 0.30000000000000004 False
print(math.isclose(0.1 + 0.2, 0.3))              # True：带容差比较
print(round(2.5), round(3.5), round(0.5))        # 2 4 0：四舍六入五成双（银行家舍入）
from fractions import Fraction
print(Fraction(1, 10) + Fraction(2, 10) == Fraction(3, 10))   # True：用分数得到精确结果
print(-17 // 5, -17 % 5, int(-17 / 5))           # -4 3 -3
```

- 能用整数就不用浮点：比例、除法判断用交叉相乘（`a * d == b * c`），LC 836、149 这类题尤其如此。
- 需要「四舍五入」时 `round` 不可靠，自己写 `int(x + 0.5)`（非负数）。
- `//` 向**负无穷**取整，`%` 的符号与除数相同；需要向 0 取整的整数除法（LC 29、166、227 里的除法）要特殊处理：`int(a / b)` 在 `|a|` 很大时会因浮点精度出错，更稳的是 `abs(a) // abs(b)` 再补符号。
- `math.ceil(a / b)` 同样经过浮点，`a` 超过 `2^53` 时不可靠；整数向上取整用 `-(-a // b)` 或 `(a + b - 1) // b`，对任意大小的整数都精确；LC 875、1011 的判定函数里常这样写。
- 对 `10^9 + 7` 取模时，Python 的 `%` 对负数返回非负结果，不像 C++ 需要 `(x % M + M) % M`。
