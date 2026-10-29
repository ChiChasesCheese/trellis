---
id: tlc-count-primes-4-followup
node: a.count-primes
type: qa
step: 4
---
## Q
**LC 204 计数质数**｜追问

面试官接着问：（1）内存能不能再省一半？（2）有没有真正 `O(n)` 的筛法，在 Python 里更快吗？（3）`n` 到 `10^9`，内存装不下怎么办？

## A
1. **只存奇数**：偶数里只有 2 是质数。下标 `i` 代表奇数 `2*i+1`，数组长度 `n // 2`，内存和划数次数都减半。
```python
from math import isqrt

def count_primes_odd(n: int) -> int:
    if n < 3:
        return 0
    size = n // 2                                    # 下标 i 代表奇数 2*i+1
    odd = bytearray([1]) * size
    odd[0] = 0                                       # 1 不是质数
    for i in range(1, (isqrt(n - 1) - 1) // 2 + 1):
        if odd[i]:
            p = 2 * i + 1
            start = (p * p) // 2                     # p*p 对应的下标
            odd[start::p] = bytes(len(range(start, size, p)))
    return sum(odd) + 1                              # 加上唯一的偶质数 2
```
`n = 5 * 10**6` 同样得到 `348513`，约 0.005 秒。
2. **线性筛（欧拉筛）**：每个合数只被它的最小质因子划一次，严格 `O(n)`；内层循环里 `i % p == 0` 时 `break`。但它在 Python 里是逐元素循环，`n = 5 * 10**6` 约 0.24 秒，比切片赋值版（约 0.01 秒）慢二十几倍。面试里说出它的思想即可，写代码用切片版。
3. **`n` 很大**：分段筛。先筛出 `sqrt(n)` 以内的质数，再把 `[0, n)` 切成每段几 MB 的块，对每块用这些质数划倍数、数质数，内存 `O(sqrt n + 块大小)`。

**Python 提醒**：`is_prime[i*i::i] = bytes(k)` 要求右边长度恰好等于切片长度，否则对扩展切片抛 `ValueError`；用 `bytes(k)`（全零的 `k` 字节）比 `[0] * k` 快五倍以上，不用先建一个 Python 列表。
