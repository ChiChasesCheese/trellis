---
id: tlc-climbing-stairs-4-followup
node: b.climbing-stairs
type: qa
step: 4
---
## Q
**LC 70 爬楼梯**｜追问

面试官接着问：（1）`n` 是 `10^18`，结果对 `10^9 + 7` 取模，怎么办？（2）每次可以爬 `1` 到 `k` 阶呢？（3）能不能不循环，给出公式？

## A
1. **矩阵快速幂**：`[[1,1],[1,0]]^n` 的左上角就是 `f(n)`，用二进制拆 `n`，`O(log n)` 次 `2 x 2` 矩阵乘法：

```python
def climb_big(n: int, mod: int = 10**9 + 7) -> int:
    def mul(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
        return [[(a[0][0] * b[0][0] + a[0][1] * b[1][0]) % mod, (a[0][0] * b[0][1] + a[0][1] * b[1][1]) % mod],
                [(a[1][0] * b[0][0] + a[1][1] * b[1][0]) % mod, (a[1][0] * b[0][1] + a[1][1] * b[1][1]) % mod]]

    result, base = [[1, 0], [0, 1]], [[1, 1], [1, 0]]
    while n:
        if n & 1:
            result = mul(result, base)
        base = mul(base, base)
        n >>= 1
    return result[0][0]
```

   `climb_big(45, 10**30)` 给出 `1836311903`（与循环版一致），`climb_big(10**18)` 给出 `680057396`。
2. **一次 `1..k` 阶**：`f(n) = f(n-1) + ... + f(n-k)`，维护最近 `k` 项的窗口和，每步加新项减旧项，`O(n)`：

```python
def climb_k(n: int, k: int) -> int:
    dp = [0] * (n + 1)
    dp[0] = 1
    window = 1                                  # window = dp[i-k .. i-1] 之和
    for i in range(1, n + 1):
        dp[i] = window
        window += dp[i]
        if i - k >= 0:
            window -= dp[i - k]
    return dp[n]
```

   `k = 2` 时就是原题（`climb_k(45, 2) = 1836311903`）；`k = 3` 时 `climb_k(3, 3) = 4`，`climb_k(4, 3) = 7`。
3. **公式**：比内公式（Binet）用到 `sqrt(5)`，浮点数在 `n` 较大时精度不够，面试里不推荐；整数循环或矩阵快速幂都精确。

**Python 提醒**：`n >>= 1` 与 `n & 1` 是位运算拆二进制的惯用法；Python 的 `int` 是任意精度，`pow(2, 10**6)` 这类运算不会溢出，但很大的乘法会慢，所以要边乘边取模。
