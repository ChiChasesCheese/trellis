---
id: tlc-patterns-dp-grid-string-1-signals
node: patterns.dp-grid-string
type: qa
step: 1
---
## Q
**动态规划：网格、双串与区间｜信号**

什么样的题面该想到二维 DP？网格路径、双字符串、回文这三类的状态分别怎么设？

## A
**二维 DP 的触发信号：**
- **网格**，只能向右 / 向下走，问路径数：`dp[r][c]` 只依赖上方和左方（例：LC 62 不同路径）。
- **两个字符串 / 序列**，问最长公共子序列、能否匹配：`dp[i][j]` 表示 `a` 的前 `i` 个与 `b` 的前 `j` 个（例：LC 1143 最长公共子序列）。
- **一个字符串**，问回文子序列：`dp[i][j]` 表示子串 `s[i..j]`（区间 DP）（例：LC 516 最长回文子序列）。
- **正方形 / 矩形**：以 `(r, c)` 为右下角的最大正方形边长（例：LC 221 最大正方形）。
- 数据范围：`m, n` 到几百到一千（`<= 500` 或 `<= 1000`），`O(mn)` 即可，约 `10^6` 个状态（例：LC 72 编辑距离）。

**四步法同样适用**：状态 → 转移 → 初值（第 0 行 / 第 0 列）→ 顺序（从小到大）。

**写法顺序**：先写完整二维表，答案对了再考虑压缩空间；压缩的条件和写法见 Python 工具箱「DP 降维」。

**近似信号：**
- 网格里**四个方向都能走** ⇒ 不是单向 DP，用 DFS 加记忆化或 BFS（例：LC 329 矩阵中的最长递增路径）。
- 要输出**具体方案**（路径本身、编辑操作序列）⇒ 保留完整二维表，再回溯（例：LC 64 最小路径和）。
- 问子串且 `n` 很大 ⇒ 中心扩展、Manacher，而不是 `O(n^2)` 空间的 DP（例：LC 5 最长回文子串）。
- 两个字符串的**子串**（连续）⇒ 状态定义为"以 `i`、`j` 结尾"，不匹配就清零（例：LC 718 最长重复子数组）。

**例题：** LC 62 不同路径

`m x n` 网格，机器人从左上角出发只能向下或向右，问到右下角的不同路径数，`1 <= m, n <= 100`。

```python
from math import comb
def unique_paths(m: int, n: int) -> int:
    dp = [[1] * n for _ in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[m - 1][n - 1]
def unique_paths_comb(m: int, n: int) -> int:
    return comb(m + n - 2, m - 1)
```

**例题：** LC 1143 最长公共子序列

返回 `text1`、`text2` 的最长公共子序列长度，`1 <= 长度 <= 1000`，仅小写字母。

```python
def longest_common_subsequence(text1: str, text2: str) -> int:
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i, a in enumerate(text1, 1):
        for j, b in enumerate(text2, 1):
            if a == b:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]
```

**例题：** LC 516 最长回文子序列

返回字符串 `s` 中最长回文子序列的长度，`1 <= s.length <= 1000`，仅小写字母。

```python
def longest_palindrome_subseq(s: str) -> int:
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        dp[i][i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    return dp[0][n - 1]
```

**例题：** LC 221 最大正方形

在由 `'0'` 和 `'1'` 组成的 `m x n` 矩阵里找只含 `'1'` 的最大正方形，返回面积，`1 <= m, n <= 300`。

```python
def maximal_square(matrix: list[list[str]]) -> int:
    m, n = len(matrix), len(matrix[0])
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    side = 0
    for i, row in enumerate(matrix, 1):
        for j, ch in enumerate(row, 1):
            if ch == "1":
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
                side = max(side, dp[i][j])
    return side * side
```

**例题：** LC 72 编辑距离

用插入、删除、替换三种操作把 `word1` 变成 `word2`，求最少操作数，`0 <= 长度 <= 500`。

```python
def min_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j - 1],
                                   dp[i - 1][j],
                                   dp[i][j - 1])
    return dp[m][n]
```

**例题：** LC 329 矩阵中的最长递增路径

在 `m x n` 整数矩阵里可向上下左右移动，求最长严格递增路径的长度，`1 <= m, n <= 200`。

```python
def longest_increasing_path(matrix: list[list[int]]) -> int:
    m, n = len(matrix), len(matrix[0])
    memo = [[0] * n for _ in range(m)]
    def dfs(i: int, j: int) -> int:
        if memo[i][j]:
            return memo[i][j]
        best = 1
        for x, y in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= x < m and 0 <= y < n and matrix[x][y] > matrix[i][j]:
                best = max(best, 1 + dfs(x, y))
        memo[i][j] = best
        return best
    return max(dfs(i, j) for i in range(m) for j in range(n))
```

**例题：** LC 64 最小路径和

非负整数网格，每次只能向下或向右，求左上角到右下角的最小路径和，`1 <= m, n <= 200`。

```python
def min_path_sum(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = grid[0][0]
    for j in range(1, n):
        dp[0][j] = dp[0][j - 1] + grid[0][j]
    for i in range(1, m):
        dp[i][0] = dp[i - 1][0] + grid[i][0]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = min(dp[i - 1][j], dp[i][j - 1]) + grid[i][j]
    return dp[m - 1][n - 1]
```

**例题：** LC 5 最长回文子串

返回字符串 `s` 中最长的回文子串，`1 <= s.length <= 1000`。

```python
def longest_palindrome(s: str) -> str:
    n = len(s)
    best_l = best_r = 0
    for center in range(2 * n - 1):
        l = center // 2
        r = l + center % 2
        while l >= 0 and r < n and s[l] == s[r]:
            l -= 1
            r += 1
        if r - l - 1 > best_r - best_l + 1:
            best_l, best_r = l + 1, r - 1
    return s[best_l : best_r + 1]
```

**例题：** LC 718 最长重复子数组

返回两个整数数组 `nums1`、`nums2` 中公共的、最长的**连续**子数组的长度，`1 <= 长度 <= 1000`。

```python
def find_length(nums1: list[int], nums2: list[int]) -> int:
    m, n = len(nums1), len(nums2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    best = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if nums1[i - 1] == nums2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                best = max(best, dp[i][j])
    return best
```
