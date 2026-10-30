---
id: tlc-edit-distance-2-code
node: p3.edit-distance
type: qa
step: 2
---
## Q
**LC 72 编辑距离**｜写出 Python 实现

两个小写字母字符串 `word1`、`word2`（长度都在 `[0, 500]`），可以对 `word1` 做插入、删除、替换一个字符的操作。返回把 `word1` 变成 `word2` 的最少操作数。

## A
**思路。** `dp[i][j]` 是 `word1[:i]` 到 `word2[:j]` 的最少操作数。第 0 行是 `0..n`（全部插入），第 0 列是 `0..m`（全部删除）。其他格子：两个末尾字符相同，取左上角；不同，取左上（替换）、上（删除）、左（插入）三者最小值加 `1`。答案是右下角 `dp[m][n]`。

```python
def min_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    # dp[i][j]：word1[:i] 变成 word2[:j] 的最少操作数
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i                        # 第 0 列：word1[:i] -> 空串，删 i 个
    for j in range(n + 1):
        dp[0][j] = j                        # 第 0 行：空串 -> word2[:j]，插 j 个
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]         # 末尾相同，不花操作
            else:
                dp[i][j] = 1 + min(dp[i - 1][j - 1],   # 替换
                                   dp[i - 1][j],       # 删除 word1[i-1]
                                   dp[i][j - 1])       # 插入 word2[j-1]
    return dp[m][n]
```

运行：`("horse", "ros")` → `3`，`("intention", "execution")` → `5`，`("", "abc")` → `3`，`("abc", "")` → `3`，`("", "")` → `0`，`("a", "a")` → `0`，两个 500 个字符的随机串也瞬间算完。

**复杂度。** 时间 `O(m · n)`：两层循环；空间 `O(m · n)`：`(m + 1) × (n + 1)` 的表。

**写法要点。** `[[0] * (n + 1) for _ in range(m + 1)]` 每行是一个新列表，第 0 行第 0 列再用两个单层循环整行整列写好；主循环从 `1` 开始，`i`、`j` 就是前缀长度，字符是 `word1[i - 1]`、`word2[j - 1]`；三个候选放进一个 `min(...)` 里并逐项写注释，对应替换 / 删除 / 插入；自底向上的写法没有递归，`m + n` 到 `1000` 时也不会像 `@cache` 的自顶向下那样触到递归上限。
