---
id: tlc-patterns-dp-grid-string-9-problems
node: patterns.dp-grid-string
type: qa
step: 9
---
## Q
**动态规划：网格、双串与区间｜本组用到二维 DP 的题**

按变形分类，这个题组里哪些题属于网格、双串或区间 DP？

## A
**网格路径**
- LC 62 不同路径
- LC 64 最小路径和
- LC 221 最大正方形

**双字符串**
- LC 1143 最长公共子序列
- LC 72 编辑距离
- LC 10 正则表达式匹配

**单字符串 / 区间**
- LC 5 最长回文子串
- LC 139 单词拆分
- LC 32 最长有效括号
- LC 140 单词拆分 II（DP 判定 + 回溯构造）
- LC 131 分割回文串（高频）

**相邻：状态里带更多信息**
- LC 3389 使字符频率相等的最少操作次数（字符计数上的 DP）
- LC 3441 变成好标题的最少代价（字符串 DP，状态含"当前字符与连续长度"）
- LC 2850 将石头分散到网格图的最少移动次数
- LC 691 贴纸拼词（高频）
- 网格中最长的之字形递增路径（高频）

提示：先定义 `dp[i][j]` 代表"前 `i` 个与前 `j` 个"还是"以 `i`、`j` 结尾"；再看末尾字符相等 / 不等时有哪几种来源；最后写完整二维表，压缩空间见 Python 工具箱「DP 降维」。

**例题：** LC 62 不同路径

机器人在 `m x n` 网格（`1 <= m, n <= 100`）的左上角，每次只能向下或向右走一步，求走到右下角的不同路径数。

```python
def unique_paths(m: int, n: int) -> int:
    dp = [[1] * n for _ in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[m - 1][n - 1]
```

**例题：** LC 64 最小路径和

给 `m x n` 的非负整数网格（`m, n <= 200`），求从左上角到右下角、每次只能向下或向右的路径上数字之和的最小值。

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

**例题：** LC 221 最大正方形

给由字符 `'0'` 和 `'1'` 组成的 `m x n` 矩阵（`m, n <= 300`），求只含 `'1'` 的最大正方形的面积。

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

**例题：** LC 1143 最长公共子序列

给两个小写字母字符串 `text1`、`text2`（长度 `<= 1000`），返回它们最长公共子序列的长度，没有则为 `0`。

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

**例题：** LC 72 编辑距离

给两个单词 `word1`、`word2`（长度 `<= 500`），求把 `word1` 变成 `word2` 所需的最少操作数；操作为插入、删除、替换一个字符。

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

**例题：** LC 10 正则表达式匹配

实现支持 `'.'`（任意单个字符）和 `'*'`（零个或多个前一个元素）的正则匹配，必须匹配整个字符串；`s` 与 `p` 的长度都 `<= 20`。

```python
from functools import cache
def is_match(s: str, p: str) -> bool:
    @cache
    def match(i: int, j: int) -> bool:
        if j == len(p):
            return i == len(s)
        first = i < len(s) and p[j] in (s[i], '.')
        if j + 1 < len(p) and p[j + 1] == '*':
            return match(i, j + 2) or (first and match(i + 1, j))
        return first and match(i + 1, j + 1)
    return match(0, 0)
```

**例题：** LC 5 最长回文子串

给字符串 `s`（`1 <= s.length <= 1000`），返回其中最长的回文子串。

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

**例题：** LC 139 单词拆分

给字符串 `s`（长度 `<= 300`）和字典 `wordDict`，判断 `s` 能否拆成一个或多个字典单词（单词可重复使用）。

```python
def word_break(s: str, word_dict: list[str]) -> bool:
    words = set(word_dict)
    max_len = max(map(len, words))
    dp = [True] + [False] * len(s)
    for i in range(1, len(s) + 1):
        dp[i] = any(dp[j] and s[j:i] in words for j in range(max(0, i - max_len), i))
    return dp[-1]
```

**例题：** LC 32 最长有效括号

给只含 `'('` 和 `')'` 的字符串 `s`（长度 `<= 3 * 10^4`），返回最长的有效（格式正确且连续）括号子串的长度。

```python
def longest_valid_parentheses(s: str) -> int:
    stack = [-1]
    best = 0
    for i, ch in enumerate(s):
        if ch == "(":
            stack.append(i)
        else:
            stack.pop()
            if stack:
                best = max(best, i - stack[-1])
            else:
                stack.append(i)
    return best
```

**例题：** LC 140 单词拆分 II

给字符串 `s`（`s.length <= 20`）和字典 `wordDict`，在 `s` 中插入空格组成句子，使每个单词都在字典里（可重复使用），返回所有这样的句子。

```python
from functools import cache
def word_break(s: str, word_dict: list[str]) -> list[str]:
    words = set(word_dict)
    max_len = max(map(len, words))
    @cache
    def sentences(i: int) -> tuple[str, ...]:
        if i == len(s):
            return ('',)
        found: list[str] = []
        for j in range(i + 1, min(len(s), i + max_len) + 1):
            if (word := s[i:j]) in words:
                for rest in sentences(j):
                    found.append(f'{word} {rest}' if rest else word)
        return tuple(found)
    return list(sentences(0))
```

**例题：** LC 3389 使字符频率相等的最少操作次数

给小写字母字符串 `s`（长度 `<= 2 * 10^4`），一次操作可以删除一个字符、添加一个字符、或把一个字符变成下一个字母（`'z'` 不能变 `'a'`）；求让所有出现过的字符次数都相等的最少操作数。

```python
from collections import Counter
from string import ascii_lowercase
def make_string_good(s: str) -> int:
    cnt = Counter(s)
    freq = [cnt[ch] for ch in ascii_lowercase]
    best = len(s)
    for t in range(1, max(freq) + 1):
        dp = [[0, 0] for _ in range(27)]
        for i in range(1, 27):
            c = freq[i - 1]
            prev = freq[i - 2] if i > 1 else 0
            short = max(t - c, 0)
            zero_prev, full_prev = dp[i - 1]
            dp[i][0] = min(zero_prev, full_prev) + c
            dp[i][1] = abs(c - t) + min(
                zero_prev - min(prev, short),
                full_prev - min(max(prev - t, 0), short),
            )
        best = min(best, *dp[26])
    return best
```

**例题：** LC 3441 变成好标题的最少代价

给小写字母字符串 `caption`（长度 `<= 5 * 10^4`），每次操作把一个字符改成相邻的前一个或后一个字母；求把它变成「每个字符都在连续至少 3 个相同字符的一组里」的最少操作数，并返回其中字典序最小的结果，做不到返回 `""`。

```python
from array import array
INF = 10**9
def min_cost_good_caption(caption: str) -> str:
    n = len(caption)
    if n < 3:
        return ""
    cap = [ord(ch) - 97 for ch in caption]
    W = 26 * 3
    h = array("i", [INF]) * (n * W)
    for c in range(26):
        h[(n - 1) * W + c * 3 + 2] = 0
    for i in range(n - 2, -1, -1):
        nxt = (i + 1) * W
        cost = [abs(cap[i + 1] - c) for c in range(26)]
        g = sorted((cost[c] + h[nxt + c * 3], c) for c in range(26))
        (g1, c1), (g2, _) = g[0], g[1]
        for c in range(26):
            base = i * W + c * 3
            for r in range(3):
                stay = cost[c] + h[nxt + c * 3 + min(r + 1, 2)]
                switch = (g2 if c == c1 else g1) if r == 2 else INF
                h[base + r] = min(stay, switch, INF)
    best = min(abs(cap[0] - c) + h[c * 3] for c in range(26))
    if best >= INF:
        return ""
    out: list[str] = []
    acc, cur, run = 0, -1, 0
    for i in range(n):
        for c in range(26):
            if i == 0:
                r = 0
            elif c == cur:
                r = min(run, 2)
            elif run == 3:
                r = 0
            else:
                continue
            step = abs(cap[i] - c)
            if acc + step + h[i * W + c * 3 + r] == best:
                out.append(chr(97 + c))
                acc, cur, run = acc + step, c, r + 1
                break
    return "".join(out)
```

**例题：** LC 2850 将石头分散到网格图的最少移动次数

`3 x 3` 网格里恰好有 `9` 个石头（一格可以有多个），每次把一个石头移到相邻格；求让每格恰好一个石头的最少移动次数。

```python
from itertools import permutations
def minimum_moves(grid: list[list[int]]) -> int:
    extra = [(r, c) for r in range(3) for c in range(3) for _ in range(grid[r][c] - 1)]
    empty = [(r, c) for r in range(3) for c in range(3) if grid[r][c] == 0]
    return min(
        sum(abs(r1 - r2) + abs(c1 - c2) for (r1, c1), (r2, c2) in zip(extra, order))
        for order in permutations(empty)
    )
```

**例题：** LC 131 分割回文串

给字符串 `s`，把它分割成若干子串，使每个子串都是回文串，返回所有可能的分割方案。`1 <= s.length <= 16`，`s` 只含小写英文字母。

```python
def partition(s: str) -> list[list[str]]:
    n = len(s)
    pal = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            pal[i][j] = s[i] == s[j] and (j - i < 2 or pal[i + 1][j - 1])
    res: list[list[str]] = []
    path: list[str] = []
    def dfs(start: int) -> None:
        if start == n:
            res.append(path.copy())
            return
        for end in range(start, n):
            if pal[start][end]:
                path.append(s[start:end + 1])
                dfs(end + 1)
                path.pop()
    dfs(0)
    return res
```

**例题：** LC 691 贴纸拼词

有 `n` 种贴纸，每张贴纸上是一个小写英文单词，每种贴纸数量无限。要拼出字符串 `target`：从贴纸上剪下单个字母，再任意重排。返回拼出 `target` 所需的最少贴纸数；做不到返回 `-1`。`n == stickers.length`，`1 <= n <= 50`，`1 <= stickers[i].length <= 10`，`1 <= target.length <= 15`，所有字符串只含小写英文字母。

```python
from collections import Counter, defaultdict
from math import inf
def min_stickers(stickers: list[str], target: str) -> int:
    n = len(target)
    full = (1 << n) - 1
    has_letter: defaultdict[str, list[Counter[str]]] = defaultdict(list)
    for s in stickers:
        cnt = Counter(s)
        for ch in cnt:
            has_letter[ch].append(cnt)
    dp = [inf] * (1 << n)
    dp[0] = 0
    for mask in range(full):
        if dp[mask] == inf:
            continue
        low = (~mask & (mask + 1)).bit_length() - 1
        for cnt in has_letter[target[low]]:
            left, new = cnt.copy(), mask
            for i, ch in enumerate(target):
                if not new >> i & 1 and left[ch] > 0:
                    left[ch] -= 1
                    new |= 1 << i
            dp[new] = min(dp[new], dp[mask] + 1)
    return -1 if dp[full] == inf else dp[full]
```

**例题：** 网格中最长的之字形递增路径

给 `m x n` 的整数网格 `grid`，一条路径从任意格子出发、每步走到上下左右相邻的格子，要求走到的值严格大于当前格子，且水平移动和竖直移动必须交替（第一步方向任意）。返回最长路径包含的格子数。`1 <= m, n <= 200`，`0 <= grid[i][j] <= 2^31 - 1`。

```python
H, V = 0, 1
STEPS = (((0, 1), (0, -1)), ((1, 0), (-1, 0)))
def longest_zigzag_path(grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    dp = [[[1] * n for _ in range(m)] for _ in range(2)]
    cells = sorted(((grid[i][j], i, j) for i in range(m) for j in range(n)), reverse=True)
    for val, i, j in cells:
        for d in (H, V):
            for di, dj in STEPS[d]:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] > val:
                    dp[d][i][j] = max(dp[d][i][j], 1 + dp[1 - d][ni][nj])
    return max(max(map(max, layer)) for layer in dp)
```
