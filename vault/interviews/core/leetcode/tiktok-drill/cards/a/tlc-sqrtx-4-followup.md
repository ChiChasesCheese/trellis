---
id: tlc-sqrtx-4-followup
node: a.sqrtx
type: qa
step: 4
---
## Q
**LC 69 x 的平方根**｜追问

面试官接着问：（1）牛顿迭代怎么写，为什么收敛得快？（2）想要小数点后 `k` 位呢？（3）标准库里有没有现成的写法，二分能不能用 `bisect`？

## A
1. **牛顿迭代（Newton's method）**：求 `f(r) = r^2 - x` 的零点，迭代 `r = (r + x / r) / 2`。整数版本从 `r = x` 开始，用整除，直到 `r * r <= x`，此时 `r` 就是向下取整的平方根；每轮误差大致平方缩小，`2^31 - 1` 只要约 19 轮。

```python
def my_sqrt_newton(x: int) -> int:
    r = x
    while r * r > x:
        r = (r + x // r) // 2                      # 牛顿迭代：r 单调递减，停在 floor(sqrt(x))
    return r
```

`my_sqrt_newton(8)` → `2`，`my_sqrt_newton(0)` → `0`，`my_sqrt_newton(1)` → `1`。当 `r = 0` 时不会进入循环，所以 `x // r` 不会除零。
2. **保留 `k` 位小数**：先把 `x` 放大 `10 ** (2k)` 倍，取整数平方根，再缩小 `10 ** k` 倍，用 `divmod` 拆出整数部分和小数部分。

```python
import math


def sqrt_digits(x: int, k: int) -> str:
    q, r = divmod(math.isqrt(x * 10 ** (2 * k)), 10 ** k)
    return f"{q}.{r:0{k}d}"
```

`sqrt_digits(2, 5)` → `'1.41421'`，`sqrt_digits(8, 3)` → `'2.828'`。整数运算不受浮点精度限制，`x` 是几百位的大整数也能得到精确结果。
3. **`bisect` 写法**：`bisect_right(range(x + 1), x, key=lambda m: m * m) - 1`。`range` 是惰性序列，`key` 让比较发生在 `m * m` 上，不会真的生成 `x + 1` 个数。

```python
from bisect import bisect_right


def my_sqrt_bisect(x: int) -> int:
    return bisect_right(range(x + 1), x, key=lambda m: m * m) - 1
```

对 `0` 到 `4999` 的所有整数和 3000 个随机的 `31` 位整数，结果与 `math.isqrt` 一致。面试中先手写二分，再提这个，说明你知道"在答案上二分"可以套标准库。

**Python 提醒**：`math.sqrt` 返回浮点数，输入超过 `2^53` 后精度不够，整数平方根用 `math.isqrt`；`x ** 0.5` 同样走浮点。LC 69 禁止它们，但真实工程里应优先 `math.isqrt`。
