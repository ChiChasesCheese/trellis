---
id: tlc-perfect-squares-4-followup
node: b.perfect-squares
type: qa
step: 4
---
## Q
**LC 279 完全平方数**｜追问

面试官接着问：（1）用 BFS 怎么做，和 DP 比如何？（2）`n` 到 `10^9` 怎么办？（3）要返回具体的拆分呢？

## A
1. **BFS**：节点是「剩余的和」，每条边减去一个平方数，从 `n` 到 `0` 的最短路层数就是答案。每层用 `set` 存余数去重；答案至多 `4`，层数很浅，实际常比 DP 快，但最坏仍要访问 `O(n)` 个余数、每个试 `√n` 条边。
2. **`n` 很大**：用数学结论，`O(√n)`。四平方和定理保证答案 `<= 4`；勒让德三平方和定理：`n` 反复除以 4 后若 `n % 8 == 7`，答案是 `4`。剩下的判断：是平方数返回 `1`，枚举 `a` 看 `n - a²` 是否为平方数返回 `2`，否则 `3`。
3. **返回拆分**：DP 时多记一个 `choice[i]`，保存取得最小值的 `j²`，最后从 `n` 沿 `choice` 回走。

```python
from math import inf, isqrt


def num_squares_path(n: int) -> list[int]:
    dp = [0] + [inf] * n
    choice = [0] * (n + 1)                  # choice[i]：取到最优时最后用的平方数
    for i in range(1, n + 1):
        for j in range(1, isqrt(i) + 1):
            if dp[i - j * j] + 1 < dp[i]:
                dp[i], choice[i] = dp[i - j * j] + 1, j * j
    res: list[int] = []
    while n:
        res.append(choice[n])
        n -= choice[n]
    return res
```

`12` → `[4, 4, 4]`，`43` → `[9, 9, 25]`。

**Python 提醒**：`int(math.sqrt(x))` 在大数上会算错，`x = (2**26 + 1)**2 - 1` 时得到 `67108865`，正确的整数平方根是 `67108864`；一律用 `math.isqrt`。
