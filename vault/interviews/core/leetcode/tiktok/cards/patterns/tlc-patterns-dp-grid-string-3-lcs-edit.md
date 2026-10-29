---
id: tlc-patterns-dp-grid-string-3-lcs-edit
node: patterns.dp-grid-string
type: qa
step: 3
---
## Q
**动态规划：网格、双串与区间｜双串模板：最长公共子序列与编辑距离**

两个字符串的 DP 状态 `dp[i][j]` 是什么？末尾字符相等和不等时分别怎么转移？

## A
`dp[i][j]` 表示 `a` 的前 `i` 个字符与 `b` 的前 `j` 个字符的答案；看两个串的**末尾字符**。

```python
def longest_common_subsequence(text1: str, text2: str) -> int:
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1        # 末尾相同：一起算进公共子序列
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])   # 丢掉任一个末尾
    return dp[m][n]

def min_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    # dp[i][j]：word1 的前 i 个字符变成 word2 的前 j 个字符的最少操作数
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i                       # 基础列：word2 为空，删掉 i 个字符
    for j in range(n + 1):
        dp[0][j] = j                       # 基础行：word1 为空，插入 j 个字符
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]            # 末尾相同：不用操作
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],       # 删除 word1 的末尾
                                   dp[i][j - 1],       # 在 word1 末尾插入
                                   dp[i - 1][j - 1])   # 替换
    return dp[m][n]
```

运行：`longest_common_subsequence("abcde", "ace")` → `3`，`("abc", "def")` → `0`；`min_distance("horse", "ros")` → `3`，`("intention", "execution")` → `5`，`("", "a")` → `1`。

- LCS 时间 `O(mn)`，空间 `O(mn)`；要还原子序列需要整张表，从 `dp[m][n]` 往回走。空间可以压到 O(n)：见 Python 工具箱「DP 降维」。
- 编辑距离三个操作对应三个方向：`dp[i-1][j]` 删除 `word1` 的末尾，`dp[i][j-1]` 在 `word1` 末尾插入，`dp[i-1][j-1]` 替换。
- 编辑距离的第 0 行 / 第 0 列：一个串为空，另一个串长度即是代价。
