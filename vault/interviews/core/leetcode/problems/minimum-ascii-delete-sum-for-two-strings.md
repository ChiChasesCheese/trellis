---
slug: minimum-ascii-delete-sum-for-two-strings
---
## Q
**LC 712 两个字符串的最小ASCII删除和**｜Medium

给两个字符串 `s1`、`s2`，每次可删除其中某个字符，代价是它的 ASCII 值。求使两个字符串相等的最小总代价。

## A
**一句话。** 类最长公共子序列的 DP：`f[i][j]` 是让 `s1` 前 `i` 个与 `s2` 前 `j` 个相等的最小删除和。

```python
def minimum_delete_sum(s1, s2):
    m, n = len(s1), len(s2)
    f = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):               # 另一边为空：全删
        f[i + 1][0] = f[i][0] + ord(s1[i])
    for j in range(n):
        f[0][j + 1] = f[0][j] + ord(s2[j])
    for i in range(m):
        for j in range(n):
            if s1[i] == s2[j]:       # 末尾相同：都保留
                f[i + 1][j + 1] = f[i][j]
            else:                    # 删 s1[i] 或删 s2[j]
                f[i + 1][j + 1] = min(
                    f[i][j + 1] + ord(s1[i]),
                    f[i + 1][j] + ord(s2[j]))
    return f[m][n]
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 边界只填 `0`：一边为空时另一边必须全删，代价是前缀 ASCII 和。
- 把代价当成 `1`：这里删每个字符代价是 ASCII 值，不能直接套编辑距离的 `+1`。

**追问。**
- 还有别的做法吗？：答案 = 两串 ASCII 总和 − 2 × 最大 ASCII 权重公共子序列。
- 删除换成只能删 `s1`（LC 583 的变形）？：保留的就是公共子序列，同一张表。

**同模式。** LC 583 两个字符串的删除操作、LC 1143 最长公共子序列、LC 72 编辑距离
