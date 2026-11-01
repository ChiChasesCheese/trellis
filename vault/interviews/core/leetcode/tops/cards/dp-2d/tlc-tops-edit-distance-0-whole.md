---
id: tlc-tops-edit-distance-0-whole
node: dp-2d.edit-distance
type: qa
---
## Q
**LC 72 编辑距离**｜Medium · 全公司热度第 110 名 · NeetCode 150、Hot 100、Top Interview 150、LeetCode 75

给你两个单词 `word1` 和 `word2`，返回把 `word1` 转换成 `word2` 所使用的最少操作数。可以对一个单词做三种操作：插入一个字符、删除一个字符、替换一个字符。`0 <= word1.length, word2.length <= 500`，只含小写英文字母。例：`"horse"` → `"ros"` 得 `3`（`horse → rorse → rose → ros`）；`"intention"` → `"execution"` 得 `5`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 双串二维 DP（Levenshtein 距离）：`dp[i][j]` 是两个前缀的最小编辑距离。

**一句话。** 末尾相同则继承 `dp[i-1][j-1]`，否则取「替换、删除、插入」三种操作中代价最小的再加 `1`。

**识别。** 「把一个字符串变成另一个，允许增删改，求最少步数」= 编辑距离；`m, n <= 500`，`O(mn)` 的二维表。

**推导。** 看两个前缀的末尾字符。相同：这一位不用操作，`dp[i-1][j-1]`。不同：三选一，替换（把 `word1[i-1]` 改成 `word2[j-1]`，退到 `(i-1, j-1)`）、删除（删掉 `word1[i-1]`，退到 `(i-1, j)`）、插入（在末尾补上 `word2[j-1]`，退到 `(i, j-1)`），各加一步，取最小。边界：空串变成长度 `j` 的串要插 `j` 次，长度 `i` 的串变空串要删 `i` 次。递归的子问题只依赖 `(i, j)`，所以用表格。

```python
def min_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    # dp[i][j]：word1[:i] 变成 word2[:j] 的最少操作数
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i  # word1[:i] 变空串：删 i 次
    for j in range(n + 1):
        dp[0][j] = j  # 空串变 word2[:j]：插 j 次
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # 末尾相同：不需要操作
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j - 1],  # 替换 word1[i-1]
                    dp[i - 1][j],  # 删除 word1[i-1]
                    dp[i][j - 1],  # 在末尾插入 word2[j-1]
                )
    return dp[m][n]
```

运行：`("horse", "ros")` → `3`；`("intention", "execution")` → `5`；`("", "a")` → `1`；`("", "")` → `0`；`("abc", "abc")` → `0`。

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。空间可以压到 `O(min(m, n))`：见 Python 工具箱「DP 降维」。

**拓展优化。**
- 还原具体操作序列：从 `dp[m][n]` 沿「来自哪个转移」回溯，逐步记下替换 / 删除 / 插入。

**易错点。**
- 忘记初始化第 0 行 / 第 0 列：`("", "a")` 会得到 `0`，正确是 `1`。
- 三种转移对应的下标容易混淆：删除退到 `dp[i-1][j]`，插入退到 `dp[i][j-1]`，替换退到 `dp[i-1][j-1]`；删除和插入写反时，不对称的样例（如 `"horse"` → `"ros"`）会得到错误的值。
- 字符相同时不要再加 `1`，也不必比较其他转移（相同时继承斜上方一定最优）。

**同模式。** LC 1143 最长公共子序列、LC 583 两个字符串的删除操作、LC 712 两个字符串的最小ASCII删除和、LC 97 交错字符串。
