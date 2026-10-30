---
id: tlc-distinct-subsequences-2-code
node: p4.distinct-subsequences
type: qa
step: 2
---
## Q
**LC 115 不同的子序列**｜写出 Python 实现

字符串 `s`、`t`（长度各在 `1` 到 `1000`，由英文字母组成）。返回 `s` 的子序列中等于 `t` 的个数（不同下标选法算不同方案）。结果保证在 32 位有符号整数范围内。要求 `O(mn)` 时间。

## A
**思路。** `dp[i][j]` 表示 `s` 的前 `i` 个字符里 `t[:j]` 的出现次数。第 0 列每一行都是 `1`（`t` 为空，什么都不选，恰有一种），第 0 行其余是 `0`。逐行填：先继承上一行同列（不用 `s[i-1]`），字符相等时再加上左上角 `dp[i-1][j-1]`（用 `s[i-1]` 去配 `t[j-1]`）。答案是 `dp[m][n]`。

```python
def num_distinct(s: str, t: str) -> int:
    m, n = len(s), len(t)
    # dp[i][j]：s[:i] 里 t[:j] 作为子序列出现的次数
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = 1                        # 空串是任何前缀的子序列，恰有一种取法
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i - 1][j]         # 不用 s[i-1]
            if s[i - 1] == t[j - 1]:
                dp[i][j] += dp[i - 1][j - 1]  # 用 s[i-1] 去配 t[j-1]
    return dp[m][n]
```

运行：`("rabbbit", "rabbit")` → `3`，`("babgbag", "bag")` → `5`，`("a", "aa")` → `0`，`("aaa", "a")` → `3`，`("abc", "abc")` → `1`，`("a" * 1000, "a" * 500)` 也瞬间算完。

**复杂度。** 时间 `O(mn)`：两层循环，每格常数；空间 `O(mn)`：`(m + 1) × (n + 1)` 的表，约一百万个整数。

**写法要点。** `[[0] * (n + 1) for _ in range(m + 1)]` 每行是一个新列表；第 0 列在单独的循环里整列置 `1`，第 0 行保持 `0`，主循环从 `1` 开始，所以 `s[i - 1]`、`t[j - 1]` 不会越界；`dp[i][j] = dp[i - 1][j]` 先写「不用」，再 `+=` 「用」，计数 DP 的转移就是加法，不需要 `max`；Python 的 `int` 不会溢出，题目保证的 32 位范围只是输出的约束。
