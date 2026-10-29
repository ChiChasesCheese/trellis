---
id: tlc-qing-wa-tiao-tai-jie-wen-ti-lcof-4-followup
node: b.qing-wa-tiao-tai-jie-wen-ti-lcof
type: qa
step: 4
---
## Q
**剑指 Offer 10- II 青蛙跳台阶问题**｜追问

面试官接着问：（1）每次可以跳 `1..n` 格中的任意格数呢？（2）`n` 大到 `10^18` 怎么办？（3）每次可跳 `1..k` 格？

## A
1. **任意格数**：`f(n) = f(n-1) + f(n-2) + ... + f(0)`，两式相减得 `f(n) = 2 f(n-1)`，即 `f(n) = 2^(n-1)`（`n >= 1`）。直观理解：中间 `n - 1` 个格子每个「落或不落」两种选择。用 `pow(2, n - 1, MOD)`。
2. **`n` 到 `10^18`**：`(f(n+1), f(n))` 等于矩阵 `[[1,1],[1,0]]` 的 `n` 次方乘 `(1, 1)`；矩阵快速幂把指数按二进制拆开，`O(log n)` 次 2×2 矩阵乘法。

```python
def mat_mul(x: list[list[int]], y: list[list[int]], mod: int) -> list[list[int]]:
    return [[(x[i][0] * y[0][j] + x[i][1] * y[1][j]) % mod for j in range(2)] for i in range(2)]


def num_ways_fast(n: int) -> int:
    MOD = 1_000_000_007
    result, base = [[1, 0], [0, 1]], [[1, 1], [1, 0]]
    while n:
        if n & 1:                        # 二进制这一位是 1：乘进结果
            result = mat_mul(result, base, MOD)
        base = mat_mul(base, base, MOD)  # 底数平方
        n >>= 1
    return result[0][0]                  # [[1,1],[1,0]]^n 的左上角就是 f(n)
```

3. **`1..k` 格**：`f(n) = f(n-1) + ... + f(n-k)`，维护长度 `k` 的窗口和，`O(n)`。

**Python 提醒**：`@functools.cache` 写递归最省事，但默认递归深度上限约 1000，`n` 再大就 `RecursionError`；循环版没有这个问题。
