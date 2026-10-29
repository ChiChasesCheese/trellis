---
id: tlc-closest-prime-numbers-in-range-2-code
node: a.closest-prime-numbers-in-range
type: qa
step: 2
---
## Q
**LC 2523 范围内最接近的两个质数**｜写出 Python 实现

给整数 `left`、`right`（`1 <= left <= right <= 10^6`），返回 `[left, right]` 内差最小的一对质数 `[num1, num2]`；差相同取 `num1` 最小的；不足两个质数时返回 `[-1, -1]`。

## A
**思路。** 用 `bytearray` 做埃氏筛，筛到 `right`；取出区间内的质数列表，用 `pairwise` 产生相邻对，`min` 按差取最小，并列时返回第一个。

```python
from itertools import pairwise
from math import isqrt


def closest_primes(left: int, right: int) -> list[int]:
    sieve = bytearray([1]) * (right + 1)       # sieve[i] == 1 表示 i 目前被认为是质数
    sieve[:2] = b"\x00\x00"                    # 0 和 1 不是质数
    for p in range(2, isqrt(right) + 1):
        if sieve[p]:
            # 从 p*p 起，p 的倍数全部划掉；切片赋值在 C 层完成，比 Python 循环快一个量级
            sieve[p * p :: p] = bytes(len(range(p * p, right + 1, p)))
    primes = [p for p in range(left, right + 1) if sieve[p]]
    if len(primes) < 2:
        return [-1, -1]
    # min 遇到并列的最小差时返回第一个，也就是 num1 最小的那一对
    a, b = min(pairwise(primes), key=lambda pair: pair[1] - pair[0])
    return [a, b]
```

**运行。** `closest_primes(10, 19)` → `[11, 13]`；`(4, 6)` → `[-1, -1]`；`(1, 1)` → `[-1, -1]`；`(1, 3)` → `[2, 3]`；`(1, 10**6)` → `[2, 3]`。

**复杂度。** 时间 `O(R log log R)`，`R = right`：每个质数 `p` 划 `R/p` 次，总和约 `R log log R`，之后扫描 `O(R)`；空间 `O(R)`，`bytearray` 每个数 1 字节。

**写法要点。** `bytearray([1]) * (right + 1)` 比 `[True] * n` 省 8 倍内存；`sieve[p*p::p] = bytes(k)` 用一次切片赋值代替内层 Python 循环，右边长度必须等于切片长度 `len(range(...))`；`math.isqrt` 是精确的整数开方，不像 `int(x ** 0.5)` 有浮点误差；`itertools.pairwise` 直接给出相邻对；`min(..., key=...)` 并列时返回先遇到的元素，这一点正好满足「`num1` 最小」。
