---
id: tlc-count-primes-2-code
node: p4.count-primes
type: qa
step: 2
---
## Q
**LC 204 计数质数**｜写出 Python 实现

整数 `n`（`0 <= n <= 5 * 10^6`），返回严格小于 `n` 的质数个数。要在一秒内跑完最大数据。

## A
**思路。** 用 `bytearray` 做筛：`is_prime[i]` 为 1 表示 `i` 还是候选。遇到仍为 1 的 `i`，把 `i*i, i*i+i, ...` 一次性置 0；`i` 枚举到 `sqrt(n-1)`。最后数组之和就是质数个数。

```python
from math import isqrt

def count_primes(n: int) -> int:
    if n < 3:
        return 0                                     # n <= 2 时没有小于 n 的质数
    is_prime = bytearray([1]) * n                    # is_prime[i] == 1 表示 i 目前仍是质数候选
    is_prime[0] = is_prime[1] = 0
    for i in range(2, isqrt(n - 1) + 1):             # 只需筛到 sqrt(n-1)
        if is_prime[i]:
            # 从 i*i 开始：更小的倍数 i*k (k<i) 已被更小的质因子划掉
            is_prime[i * i::i] = bytes(len(range(i * i, n, i)))
    return sum(is_prime)
```

运行：`10` → `4`，`0` → `0`，`1` → `0`，`2` → `0`，`3` → `1`，`5 * 10**6` → `348513`（约 0.01 秒）。

**复杂度。** 时间 `O(n log log n)`，质数 `p` 划 `n/p` 个，对质数求和得 `n log log n`；空间 `O(n)`，约 `n` 字节。

**写法要点。** `bytearray([1]) * n` 一次建好；`isqrt` 是整数开方，不会像 `int(n ** 0.5)` 在大数上有浮点误差；切片赋值 `a[s::i] = bytes(k)` 在 C 层一次完成，`k` 必须恰好等于切片长度，所以用 `len(range(i*i, n, i))` 算；`sum(bytearray)` 直接数 1 的个数。
