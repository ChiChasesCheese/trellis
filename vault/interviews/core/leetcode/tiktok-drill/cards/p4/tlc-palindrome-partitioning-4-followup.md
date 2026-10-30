---
id: tlc-palindrome-partitioning-4-followup
node: p4.palindrome-partitioning
type: qa
step: 4
---
## Q
**LC 131 分割回文串**｜追问

字符串 `s` 的全部回文分割方案已经用「回文表加回溯」求出。面试官接着问：（1）只要最少切几刀（LC 132）？（2）只要方案总数？（3）`s` 长到 `10^3`，回溯还可行吗？（4）输出顺序有要求吗？

## A
1. **最少切割次数**：同一张回文表，再做一维 DP。`dp[j]` 是 `s[:j+1]` 的最少切割次数：整段回文则为 `0`，否则取所有满足 `pal[i][j]` 的 `i` 的 `dp[i-1] + 1` 的最小值。

```python
def min_cut(s: str) -> int:
    n = len(s)
    pal = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            pal[i][j] = s[i] == s[j] and (j - i < 2 or pal[i + 1][j - 1])
    dp = [0] * n                                   # dp[j]：s[:j+1] 的最少切割次数
    for j in range(n):
        dp[j] = 0 if pal[0][j] else min(dp[i - 1] + 1 for i in range(1, j + 1) if pal[i][j])
    return dp[-1]
```

   `"aab"` → `1`，`"a"` → `0`，`"ab"` → `1`，`"abacdc"` → `1`。时间 `O(n^2)`。
2. **方案数**：不存路径，`count(start)` 表示 `s[start:]` 的方案数，`count(n) = 1`，`count(start) = sum(count(end + 1) for end if pal[start][end])`，用 `functools.cache` 记忆化，`O(n^2)`。
3. **`n = 10^3`**：全部方案的个数是指数级，不可能枚举；这个规模只会问最少切割次数或方案数，必须用 `O(n^2)` 的回文表加 DP，回溯不可行。
4. **顺序**：本解按第一段由短到长的顺序产出方案，字典序没有保证；有要求时对结果 `sort`，或按子串的字典序枚举。

**Python 提醒**：递归深度最多 `n`，`n = 10^3` 的 DP 写成递归会触发递归上限，要么迭代，要么 `sys.setrecursionlimit`；`path.copy()` 只拷贝一层，路径里是不可变的字符串，所以足够。
