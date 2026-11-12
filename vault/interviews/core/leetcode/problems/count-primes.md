---
slug: count-primes
---
## Q
**LC 204 计数质数**｜Medium

返回严格小于 `n` 的质数个数，`n` 最大 `5×10^6`。

## A
**一句话。** 埃氏筛：遇到仍是质数的 `i` 就划掉 `i*i` 起的所有倍数，`i` 只枚举到 `sqrt(n-1)`。

```python
def count_primes(n):
    if n < 3:
        return 0
    p = bytearray([1]) * n
    p[0] = p[1] = 0
    for i in range(2, isqrt(n - 1) + 1):
        if p[i]:
            # 从 i*i 起：更小的倍数已被小质因子划掉
            p[i*i::i] = bytes(len(range(i*i, n, i)))
    return sum(p)
```

**复杂度。** 时间 `O(n log log n)`，空间 `O(n)`。

**易错点。**
- 外层上界写成 `isqrt(n)`：`n = 10` 时 `range(2, 3)` 只处理 `2`，`9` 没被划掉，得 `5`，应为 `4`。
- 数组开成 `n + 1`：「小于 `n`」不含 `n`，`n = 2` 应返回 `0`。

**追问。**
- 内存装不下怎么办？：分段筛，先筛出 `sqrt(n)` 以内的质数，再分块划。
- 判断单个很大的数是否质数？：试除到 `sqrt`，或 Miller-Rabin。

**同模式。** LC 263 丑数、LC 264 丑数 II、LC 1175 质数排列、LC 762 二进制表示中质数个数的数字
