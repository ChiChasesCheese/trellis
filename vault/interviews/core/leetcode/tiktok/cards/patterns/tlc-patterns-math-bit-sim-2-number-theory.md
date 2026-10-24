---
id: tlc-patterns-math-bit-sim-2-number-theory
node: patterns.math-bit-sim
type: qa
step: 2
---
## Q
**数学、位运算与模拟｜数论：最大公约数、快速幂、水壶问题、字符串的最大公因子**

`math.gcd` 能用在哪些题上？快速幂怎样把幂降到 `O(log n)`？

## A
**LC 365 水壶问题**：容量 `x`、`y`，能量出的水量恰是 `gcd(x, y)` 的倍数（裴蜀定理，Bézout's Lemma），且不超过 `x + y`。

**LC 1071 字符串的最大公因子**：两个串有公共"因子"当且仅当 `s + t == t + s`；此时最长因子的长度是 `gcd(len(s), len(t))`。

```python
from math import gcd
def can_measure_water(x: int, y: int, target: int) -> bool:
    if target > x + y:
        return False                       # 两个壶加起来都装不下
    return target % gcd(x, y) == 0

def gcd_strings(str1: str, str2: str) -> str:
    if str1 + str2 != str2 + str1:
        return ""                          # 有公共因子的充要条件：两种拼接顺序相同
    return str1[:gcd(len(str1), len(str2))]

def pow_mod(a: int, b: int, mod: int) -> int:
    result, a = 1, a % mod
    while b:
        if b & 1:
            result = result * a % mod      # 当前二进制位是 1：乘进结果
        a = a * a % mod                    # 平方：a, a^2, a^4, ...
        b >>= 1
    return result
print(can_measure_water(3, 5, 4), can_measure_water(2, 6, 5), can_measure_water(2, 6, 9))   # True False False
print(repr(gcd_strings("ABCABC", "ABC")), repr(gcd_strings("ABABAB", "ABAB")), repr(gcd_strings("AAAAAB", "AAA")))   # 'ABC' 'AB' ''
print(pow_mod(2, 10, 1000), pow(2, 10, 1000))   # 24 24
```

- Python 内置：`math.gcd(a, b, ...)` 支持多个参数，`math.lcm`；三参数 `pow(a, b, mod)` 就是快速幂，面试中先说内置、被要求时手写。
- 快速幂把指数按二进制拆开：`b` 有 `log b` 位，每位至多两次乘法，`O(log b)`；对 `10^9 + 7` 取模时每次乘法后都取模。
- 欧几里得算法：`gcd(a, b) = gcd(b, a % b)`，`O(log min(a, b))`。
- 最小公倍数 `lcm(a, b) = a // gcd(a, b) * b`，先除后乘，避免大数（Python 无溢出，其他语言要注意）。
