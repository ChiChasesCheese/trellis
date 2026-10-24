---
id: tlc-patterns-math-bit-sim-3-sieve
node: patterns.math-bit-sim
type: qa
step: 3
---
## Q
**数学、位运算与模拟｜埃氏筛：范围内最接近的两个质数（LC 2523）**

`right` 到 `10^6`，怎样一次筛出所有质数？用什么数据结构最快？

## A
埃氏筛（Sieve of Eratosthenes）：从 `2` 开始，每遇到质数 `p`，把 `p·p, p·p+p, ...` 全部划掉。只需处理到 `√right`。

```python
import math
def closest_primes(left: int, right: int) -> list[int]:
    sieve = bytearray([1]) * (right + 1)   # 1 表示可能是质数
    sieve[0:2] = b"\x00\x00"               # 0 和 1 不是质数
    for p in range(2, math.isqrt(right) + 1):
        if sieve[p]:
            sieve[p * p::p] = bytearray(len(range(p * p, right + 1, p)))   # 切片赋值，一次划掉所有倍数
    primes = [i for i in range(max(left, 2), right + 1) if sieve[i]]
    best = [-1, -1]
    gap = float("inf")
    for a, b in zip(primes, primes[1:]):
        if b - a < gap:                    # 严格小于：并列时保留 nums1 最小的
            gap, best = b - a, [a, b]
    return best
print(closest_primes(10, 19), closest_primes(4, 6), closest_primes(1, 10**6))   # [11, 13] [-1, -1] [2, 3]
```

- 时间 `O(n log log n)`，空间 `O(n)`；`n = 10^6` 在 Python 里不到 1 秒。
- 用 `bytearray` + 切片赋值，把"划掉倍数"的内层循环交给 C 层，比 Python 里写 `for` 快一个数量级。
- 筛法从 `p·p` 开始：更小的倍数已经被更小的质数划掉。
- 对每个数单独判质数（试除到 `√n`）是 `O(√n)`，查询很多次时太慢；范围查询用筛，单个大数用试除或 Miller-Rabin。
- 相邻质数之间才可能有最小差距，所以只比较 `zip(primes, primes[1:])` 的相邻对。
- `left = 1` 时要把下界抬到 `2`（`max(left, 2)`），`1` 不是质数。
