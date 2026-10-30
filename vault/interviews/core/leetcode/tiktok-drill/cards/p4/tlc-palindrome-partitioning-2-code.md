---
id: tlc-palindrome-partitioning-2-code
node: p4.palindrome-partitioning
type: qa
step: 2
---
## Q
**LC 131 分割回文串**｜写出 Python 实现

给字符串 `s`（`1 <= len(s) <= 16`，只含小写字母），返回把它分割成若干回文子串的所有方案，每个方案是子串的列表。

## A
**思路。** 先用区间 DP 填 `pal[i][j]`；再 `dfs(start)` 枚举第一段 `s[start:end+1]`，只有它是回文才加入 `path` 并递归 `end + 1`；`start == n` 时把 `path` 的拷贝收进结果，回溯时 `pop` 撤销。

```python
def partition(s: str) -> list[list[str]]:
    n = len(s)
    pal = [[False] * n for _ in range(n)]    # pal[i][j]：s[i..j] 是否回文
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            pal[i][j] = s[i] == s[j] and (j - i < 2 or pal[i + 1][j - 1])
    res: list[list[str]] = []
    path: list[str] = []

    def dfs(start: int) -> None:
        if start == n:
            res.append(path.copy())          # 必须拷贝：path 之后还会被修改
            return
        for end in range(start, n):
            if pal[start][end]:
                path.append(s[start:end + 1])
                dfs(end + 1)
                path.pop()                   # 回溯

    dfs(0)
    return res
```

运行：`"aab"` → `[['a', 'a', 'b'], ['aa', 'b']]`，`"a"` → `[['a']]`，`"aba"` → `[['a', 'b', 'a'], ['aba']]`，`"a" * 16` → `32768` 种方案。

**复杂度。** 预处理 `O(n^2)`；搜索最坏 `O(n · 2^n)`：全是同一字符时有 `2^(n-1)` 个方案，每个方案拷贝 `O(n)`；空间 `O(n^2)` 回文表加 `O(n)` 递归栈，输出不计。

**写法要点。**
- `pal[i][j] = s[i] == s[j] and (j - i < 2 or pal[i + 1][j - 1])`：布尔表达式短路，`j - i < 2` 时不再读 `pal[i + 1][j - 1]`，避免越界和读到没算的值。
- `path.copy()`（或 `path[:]`）：收集结果必须存快照；`path` 是被反复修改的同一个列表。
- 内层函数 `dfs` 直接读写外层的 `res`、`path`，不需要作为参数传递；`path` 用 `append`/`pop` 原地修改，比每层 `path + [x]` 新建列表省拷贝。
- 想少写预处理：`@functools.cache` 修饰 `is_pal(i, j)`，`n <= 16` 足够；`n` 大时显式的二维表更快。
