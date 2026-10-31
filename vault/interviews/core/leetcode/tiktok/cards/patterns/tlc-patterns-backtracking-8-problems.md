---
id: tlc-patterns-backtracking-8-problems
node: patterns.backtracking
type: qa
step: 8
---
## Q
**回溯（Backtracking）｜本组用到回溯的题**

按变形分类，这个题组里哪些题属于回溯？

## A
**子集 / 组合**
- LC 78 子集
- LC 77 组合
- LC 39 组合总和
- LC 40 组合总和 II（排序 + 同层去重）
- LC 1239 串联字符串的最大长度（高频）

**排列**
- LC 46 全排列

**约束摆放 / 网格**
- LC 51 N 皇后
- LC 79 单词搜索
- 枚举有向图中的所有简单路径（高频）
- LC 212 单词搜索 II（回溯 + 字典树）

**字符串生成 / 分割**
- LC 22 括号生成
- LC 93 复原 IP 地址
- LC 301 删除无效的括号（回溯或 BFS）
- LC 140 单词拆分 II（回溯 + 记忆化）
- LC 131 分割回文串（高频）
- 有效括号字符串：判断，并输出全部方案（高频）

提示：先写出"每一步的选择是什么、终点是什么、怎样剪枝"；再决定下一层的起点（`i` 还是 `i + 1`）、是否需要排序去重、是否能改成 DP。

**例题：** LC 78 子集

给一个元素互不相同的整数数组 `nums`（`1 <= nums.length <= 10`），返回所有子集（幂集），不含重复子集，顺序任意。

```python
def subsets(nums: list[int]) -> list[list[int]]:
    res: list[list[int]] = []
    path: list[int] = []
    def dfs(start: int) -> None:
        res.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            dfs(i + 1)
            path.pop()
    dfs(0)
    return res
```

**例题：** LC 77 组合

给整数 `n` 和 `k`（`1 <= k <= n <= 20`），返回 `[1, n]` 中所有 `k` 个数的组合，顺序任意。

```python
def combine(n: int, k: int) -> list[list[int]]:
    res: list[list[int]] = []
    path: list[int] = []
    def dfs(start: int) -> None:
        if len(path) == k:
            res.append(path[:])
            return
        need = k - len(path)
        for x in range(start, n - need + 2):
            path.append(x)
            dfs(x + 1)
            path.pop()
    dfs(1)
    return res
```

**例题：** LC 39 组合总和

给无重复元素的数组 `candidates`（`2 <= candidates[i] <= 40`）和目标 `target`（`<= 40`），找出和为 `target` 的所有不同组合；同一个数可以重复选取任意次。

```python
def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    candidates = sorted(candidates)
    result: list[list[int]] = []
    path: list[int] = []
    def dfs(start: int, remain: int) -> None:
        if remain == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            x = candidates[i]
            if x > remain:
                break
            path.append(x)
            dfs(i, remain - x)
            path.pop()
    dfs(0, target)
    return result
```

**例题：** LC 40 组合总和 II

给可能有重复元素的数组 `candidates`（长度 `<= 100`）和 `target`（`<= 30`），找出和为 `target` 的所有不重复组合；每个元素在一个组合里最多用一次。

```python
def combination_sum2(candidates: list[int], target: int) -> list[list[int]]:
    nums = sorted(candidates)
    result: list[list[int]] = []
    path: list[int] = []
    def dfs(start: int, remain: int) -> None:
        if remain == 0:
            result.append(path[:])
            return
        for i in range(start, len(nums)):
            if nums[i] > remain:
                break
            if i > start and nums[i] == nums[i - 1]:
                continue
            path.append(nums[i])
            dfs(i + 1, remain - nums[i])
            path.pop()
    dfs(0, target)
    return result
```

**例题：** LC 46 全排列

给不含重复数字的数组 `nums`（`1 <= nums.length <= 6`），返回所有全排列，顺序任意。

```python
def permute(nums: list[int]) -> list[list[int]]:
    n = len(nums)
    res: list[list[int]] = []
    path: list[int] = []
    used = [False] * n
    def dfs() -> None:
        if len(path) == n:
            res.append(path[:])
            return
        for i, x in enumerate(nums):
            if used[i]:
                continue
            used[i] = True
            path.append(x)
            dfs()
            path.pop()
            used[i] = False
    dfs()
    return res
```

**例题：** LC 51 N 皇后

在 `n x n` 棋盘（`1 <= n <= 9`）上放 `n` 个互不攻击（同行、同列、同斜线都不行）的皇后，返回所有摆法；每种摆法是 `n` 个字符串，`'Q'` 为皇后、`'.'` 为空位。

```python
def solve_n_queens(n: int) -> list[list[str]]:
    result: list[list[str]] = []
    cols: list[int] = []
    used_col: set[int] = set()
    used_diag: set[int] = set()
    used_anti: set[int] = set()
    def place(r: int) -> None:
        if r == n:
            result.append(["." * c + "Q" + "." * (n - c - 1) for c in cols])
            return
        for c in range(n):
            if c in used_col or r - c in used_diag or r + c in used_anti:
                continue
            cols.append(c)
            used_col.add(c)
            used_diag.add(r - c)
            used_anti.add(r + c)
            place(r + 1)
            used_anti.remove(r + c)
            used_diag.remove(r - c)
            used_col.remove(c)
            cols.pop()
    place(0)
    return result
```

**例题：** LC 79 单词搜索

给字符网格 `board`（`m, n <= 6`）和字符串 `word`（长度 `<= 15`），判断 `word` 能否沿水平或竖直相邻的格子拼出，同一格在一条路径里不能重复使用。

```python
from collections import Counter
from itertools import chain
def exist(board: list[list[str]], word: str) -> bool:
    rows, cols = len(board), len(board[0])
    board_count = Counter(chain.from_iterable(board))
    if Counter(word) - board_count:
        return False
    if board_count[word[0]] > board_count[word[-1]]:
        word = word[::-1]
    def dfs(r: int, c: int, k: int) -> bool:
        if board[r][c] != word[k]:
            return False
        if k == len(word) - 1:
            return True
        board[r][c] = "#"
        found = any(
            0 <= nr < rows and 0 <= nc < cols and dfs(nr, nc, k + 1)
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1))
        )
        board[r][c] = word[k]
        return found
    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))
```

**例题：** LC 212 单词搜索 II

给 `m x n` 的字符网格（`m, n <= 12`）和单词列表 `words`（最多 `3 * 10^4` 个，每个长度 `<= 10`），返回所有能在网格里按相邻格拼出的单词，同一格在一个单词里不能重复使用。

```python
from typing import Any
def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    root: dict[str, Any] = {}
    for word in words:
        node = root
        for ch in word:
            node = node.setdefault(ch, {})
        node['$'] = word
    m, n = len(board), len(board[0])
    found: list[str] = []
    def dfs(i: int, j: int, parent: dict[str, Any]) -> None:
        ch = board[i][j]
        node = parent[ch]
        if word := node.pop('$', None):
            found.append(word)
        board[i][j] = '#'
        for ni, nj in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= ni < m and 0 <= nj < n and board[ni][nj] in node:
                dfs(ni, nj, node)
        board[i][j] = ch
        if not node:
            del parent[ch]
    for i in range(m):
        for j in range(n):
            if board[i][j] in root:
                dfs(i, j, root)
    return found
```

**例题：** LC 22 括号生成

给整数 `n`（`1 <= n <= 8`），生成所有由 `n` 对括号组成的有效括号串。

```python
def generate_parenthesis(n: int) -> list[str]:
    res: list[str] = []
    path: list[str] = []
    def dfs(opened: int, closed: int) -> None:
        if len(path) == 2 * n:
            res.append("".join(path))
            return
        if opened < n:
            path.append("(")
            dfs(opened + 1, closed)
            path.pop()
        if closed < opened:
            path.append(")")
            dfs(opened, closed + 1)
            path.pop()
    dfs(0, 0)
    return res
```

**例题：** LC 93 复原 IP 地址

给只含数字的字符串 `s`（`1 <= s.length <= 20`），在其中插入三个 `.`，返回所有有效 IP 地址：四段整数各在 `0..255`，且不能有前导 0。

```python
def restore_ip_addresses(s: str) -> list[str]:
    n = len(s)
    res: list[str] = []
    parts: list[str] = []
    def dfs(start: int) -> None:
        left = 4 - len(parts)
        if left == 0:
            if start == n:
                res.append(".".join(parts))
            return
        if not left <= n - start <= 3 * left:
            return
        for end in range(start + 1, min(start + 3, n) + 1):
            seg = s[start:end]
            if len(seg) > 1 and seg[0] == "0":
                break
            if int(seg) > 255:
                break
            parts.append(seg)
            dfs(end)
            parts.pop()
    dfs(0)
    return res
```

**例题：** LC 301 删除无效的括号

给由小写字母和括号组成的字符串 `s`（`s.length <= 25`，括号至多 `20` 个），删除最少数量的括号使它有效，返回所有不重复的结果，顺序任意。

```python
def remove_invalid_parentheses(s: str) -> list[str]:
    left_rem = right_rem = 0
    for ch in s:
        if ch == "(":
            left_rem += 1
        elif ch == ")":
            if left_rem:
                left_rem -= 1
            else:
                right_rem += 1
    delta = {"(": 1, ")": -1}
    res: set[str] = set()
    path: list[str] = []
    def dfs(i: int, left: int, right: int, balance: int) -> None:
        if left < 0 or right < 0 or balance < 0 or left + right > len(s) - i:
            return
        if i == len(s):
            if left == right == balance == 0:
                res.add("".join(path))
            return
        ch = s[i]
        if ch == "(":
            dfs(i + 1, left - 1, right, balance)
        elif ch == ")":
            dfs(i + 1, left, right - 1, balance)
        path.append(ch)
        dfs(i + 1, left, right, balance + delta.get(ch, 0))
        path.pop()
    dfs(0, left_rem, right_rem, 0)
    return list(res)
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

**例题：** LC 1239 串联字符串的最大长度

给字符串数组 `arr`。从中选出若干个字符串（保持原有顺序）连接成字符串 `s`，要求 `s` 中**所有字母各不相同**。返回所有可行的 `s` 中最长的长度（什么都不选时 `s` 为空串，长度 `0`）。`1 <= arr.length <= 16`，`1 <= arr[i].length <= 26`，`arr[i]` 只含小写字母。

```python
def max_length(arr: list[str]) -> int:
    masks = {0}
    best = 0
    for s in arr:
        if len(set(s)) < len(s):
            continue
        cur = 0
        for ch in s:
            cur |= 1 << (ord(ch) - 97)
        for m in list(masks):
            if m & cur == 0:
                masks.add(m | cur)
                best = max(best, (m | cur).bit_count())
    return best
```

**例题：** 枚举有向图中的所有简单路径（含环的情况）

给一个有向图：`n` 个点（编号 `0 .. n-1`）和边表 `edges`（`[u, v]` 表示 `u → v`，没有重边），以及起点 `s`、终点 `t`（`s != t`）。按任意顺序返回从 `s` 到 `t` 的**所有简单路径**：路径上不能重复经过同一个点。`1 <= n <= 15`，边数 `<= 60`，图里**可能有环**。

```python
from collections import deque
def all_simple_paths(n: int, edges: list[list[int]], s: int, t: int) -> list[list[int]]:
    graph: list[list[int]] = [[] for _ in range(n)]
    rev: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        rev[v].append(u)
    reach = [False] * n
    reach[t] = True
    queue = deque([t])
    while queue:
        v = queue.popleft()
        for u in rev[v]:
            if not reach[u]:
                reach[u] = True
                queue.append(u)
    paths: list[list[int]] = []
    path = [s]
    on_path = [False] * n
    on_path[s] = True
    def dfs(u: int) -> None:
        if u == t:
            paths.append(path.copy())
            return
        for v in graph[u]:
            if not on_path[v] and reach[v]:
                on_path[v] = True
                path.append(v)
                dfs(v)
                path.pop()
                on_path[v] = False
    if reach[s]:
        dfs(s)
    return paths
```

**例题：** 有效括号字符串：判断，并输出全部方案

字符串 `s` 只含 `'('`、`')'` 和 `'*'`，`'*'` 可以当作 `'('`、`')'` 或空串。第一问：判断 `s` 能否变成有效的括号字符串（括号正确配对，空串也有效），`1 <= len(s) <= 100`。第二问：输出所有**不同的**有效字符串（每个 `'*'` 取三种之一，结果去重），按字典序返回，`1 <= len(s) <= 20`。

```python
from functools import cache
def check_valid(s: str) -> bool:
    """LC 678：'*' 可当 '('、')' 或空串。lo..hi 是「未匹配左括号数」所有可能取值的范围（中间的值都能取到）。"""
    lo = hi = 0
    for ch in s:
        if ch == "(":
            lo, hi = lo + 1, hi + 1
        elif ch == ")":
            lo, hi = lo - 1, hi - 1
        else:
            lo, hi = lo - 1, hi + 1
        if hi < 0:
            return False
        lo = max(lo, 0)
    return lo == 0
def all_valid(s: str) -> list[str]:
    """所有不同的有效字符串（'*' 替换后的结果），按字典序返回。"""
    n = len(s)
    @cache
    def tails(i: int, bal: int) -> frozenset[str]:
        """s[i:] 在已有 bal 个未匹配左括号的前提下，所有能配平的替换结果。"""
        if bal > n - i:
            return frozenset()
        if i == n:
            return frozenset({""}) if bal == 0 else frozenset()
        ch = s[i]
        result: set[str] = set()
        if ch in "(*":
            result |= {"(" + t for t in tails(i + 1, bal + 1)}
        if ch in ")*" and bal > 0:
            result |= {")" + t for t in tails(i + 1, bal - 1)}
        if ch == "*":
            result |= tails(i + 1, bal)
        return frozenset(result)
    return sorted(tails(0, 0))
```
