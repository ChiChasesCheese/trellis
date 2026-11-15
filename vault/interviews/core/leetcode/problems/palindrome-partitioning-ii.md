---
slug: palindrome-partitioning-ii
---
## Q
**LC 132 分割回文串 II**｜Hard

把字符串 `s` 分割成若干子串，使每个子串都是回文，返回最少的分割次数。

## A
**一句话。** 先用区间 DP 预处理所有子串是否为回文，再用线性 DP：`f[j]` 是 `s[:j + 1]` 的最少分割次数，枚举最后一段的起点。

```python
def min_cut(s):
    n = len(s)
    is_pal = [[True] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            is_pal[i][j] = (s[i] == s[j]
                            and is_pal[i + 1][j - 1])
    f = [0] * n                  # f[j]：s[:j+1] 的最少切数
    for j in range(n):
        if is_pal[0][j]:
            continue             # 整段就是回文，不用切
        f[j] = min(f[i - 1] + 1
                   for i in range(1, j + 1) if is_pal[i][j])
    return f[n - 1]
```

**复杂度。** 时间 `O(n^2)`，空间 `O(n^2)`。

**易错点。**
- 每次转移都现场判断回文：整体变成 `O(n^3)`，要先预处理成表。
- 回文表的遍历顺序：`is_pal[i][j]` 依赖 `is_pal[i + 1][j - 1]`，`i` 要倒序。
- 相邻两个字符时 `i + 1 > j - 1`：表里下三角初值为 `True`，刚好表示空串是回文。

**追问。**
- 能降到 `O(n)` 空间吗？：用中心扩展，对每个回文中心更新 `f`，空间 `O(n)`。
- 和 LC 131 的区别？：131 要列出所有分割方案，用回溯；这里只要最少次数，用 DP。

**同模式。** LC 131 分割回文串、LC 5 最长回文子串、LC 647 回文子串
