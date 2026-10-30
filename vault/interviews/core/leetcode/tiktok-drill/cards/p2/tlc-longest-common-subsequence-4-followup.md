---
id: tlc-longest-common-subsequence-4-followup
node: p2.longest-common-subsequence
type: qa
step: 4
---
## Q
**LC 1143 最长公共子序列**｜追问

面试官接着问：（1）要返回 LCS **字符串本身**怎么办？（2）两个序列各有 `10^5` 个元素，但其中一个的元素互不相同，还能更快吗？（3）和编辑距离（LC 72）是什么关系？（4）表太大怎么办？

## A
1. **返回字符串。** 完整的二维表就是回溯的依据，从右下角回溯：
```python
def lcs_string(a: str, b: str) -> str:
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            dp[i + 1][j + 1] = dp[i][j] + 1 if a[i] == b[j] else max(dp[i][j + 1], dp[i + 1][j])
    i, j, out = m, n, []
    while i and j:
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1]); i -= 1; j -= 1       # 相等：这个字符在 LCS 里，斜着退
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1                                       # 往值更大的一侧走
        else:
            j -= 1
    return "".join(reversed(out))
```
`lcs_string("abcde", "ace")` → `"ace"`。
2. **一个序列元素互不相同。** 用字典把另一个序列映射到该序列里的位置，丢掉不在其中的元素，LCS 就变成这个位置序列的最长严格递增子序列（LIS），用二分维护 `tails`，`O(n log n)`。
3. **与编辑距离。** 只允许插入和删除的编辑距离等于 `m + n - 2 * LCS`（LC 583）；LC 72 多了替换，转移里要比较三个方向。
4. 空间可以压到 O(min(m, n))：见 Python 工具箱「DP 降维」。

**Python 提醒**：建二维表要写 `[[0] * (n + 1) for _ in range(m + 1)]`；写成 `[[0] * (n + 1)] * (m + 1)` 会让所有行是同一个列表对象，改一格全变。
