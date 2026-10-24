---
id: tlc-longest-common-subsequence-2-code
node: a.longest-common-subsequence
type: qa
step: 2
---
## Q
**LC 1143 最长公共子序列**｜写出 Python 实现

两个只含小写字母的字符串 `text1`、`text2`（长度各 1 到 1000），返回最长公共子序列的长度，不存在返回 `0`。要求 `O(mn)` 时间，并把空间压到 `O(min(m, n))`。

## A
**思路。** `dp[j]` 表示当前处理到 `text1` 的第 `i` 个字符时，与 `text2` 前 `j` 个字符的 LCS 长度。逐行更新：末尾字符相等取左上角加一，不等取「上」与「左」的较大者。左上角在被覆盖前存进 `diag`。

```python
def longest_common_subsequence(text1: str, text2: str) -> int:
    if len(text1) < len(text2):
        text1, text2 = text2, text1          # 让 text2 是较短的一条，滚动数组只有 min(m, n) + 1 长
    dp = [0] * (len(text2) + 1)              # dp[j]：当前行 text1[:i] 与 text2[:j] 的 LCS 长度
    for a in text1:
        diag = 0                             # 左上角 dp[i-1][j-1]，行首是 0
        for j, b in enumerate(text2, 1):
            diag, dp[j] = dp[j], (diag + 1 if a == b else max(dp[j], dp[j - 1]))
    return dp[-1]
```

运行：`("abcde", "ace")` → `3`，`("abc", "abc")` → `3`，`("abc", "def")` → `0`，`("a", "a")` → `1`，`("bl", "yby")` → `1`，两个 1000 个 `"a"` 的串 → `1000`。

**复杂度。** 时间 `O(mn)`：外层 `m` 次、内层 `n` 次，每格常数；空间 `O(min(m, n))`：一行数组加两个变量。

**写法要点。**
- `diag, dp[j] = dp[j], (...)`：元组赋值先算完右边，再同时赋值，右边用的 `dp[j]` 还是上一行的旧值，不用临时变量；`dp[j - 1]` 此时已是本行的新值。
- `enumerate(text2, 1)` 让下标从 1 开始，`dp[0]` 保留为「空前缀」的 0。
- 先把较短的串放在内层，数组长度取 `min(m, n) + 1`。
- `for a in text1` 直接迭代字符，不需要下标 `i`。
