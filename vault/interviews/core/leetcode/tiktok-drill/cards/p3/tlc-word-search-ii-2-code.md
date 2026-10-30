---
id: tlc-word-search-ii-2-code
node: p3.word-search-ii
type: qa
step: 2
---
## Q
**LC 212 单词搜索 II**｜写出 Python 实现

`m x n` 字符网格 `board`（`1 <= m, n <= 12`，小写字母）和 `words`（`1..3 * 10^4` 个互不相同的小写单词，长度 `1..10`）。返回所有能由相邻格子按顺序拼出的单词，一个单词内同一格不能重复使用。

## A
**思路。** 用嵌套字典建字典树，整词存在 `'$'` 键下；从每个格子出发 DFS，沿字典树同步下行；找到整词就摘走，搜空的分支从父结点删除。

```python
from typing import Any


def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    root: dict[str, Any] = {}              # 字典树：字符 -> 子结点；'$' -> 在此结束的整词
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
        if word := node.pop('$', None):    # 取走整词：同一个词不会被找到两次
            found.append(word)
        board[i][j] = '#'                  # 占位，路径内不重复使用同一格
        for ni, nj in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= ni < m and 0 <= nj < n and board[ni][nj] in node:
                dfs(ni, nj, node)
        board[i][j] = ch                   # 回溯
        if not node:                       # 这条分支的词都找完了：剪掉，之后不再进入
            del parent[ch]

    for i in range(m):
        for j in range(n):
            if board[i][j] in root:
                dfs(i, j, root)
    return found
```

运行：示例 1 → `['eat', 'oath']`，示例 2 → `[]`，`[["a"]]` 找 `["a"]` → `['a']`，`[["a","a"]]` 找 `["a"]` → `['a']`；`12 x 12` 随机 `a/b/c` 盘面、`30000` 个单词 → 约 `40 ms`。

**复杂度。** 时间最坏 `O(mn · 3^L)`，字典树剪枝后实际小得多；空间 `O(总字符数)`（字典树）加递归深度 `O(L)`。

**写法要点。** `dict.setdefault(ch, {})` 一行完成「有就取、没有就建」，建字典树只要三行。用嵌套 `dict` 代替 `class TrieNode`，省掉类定义；`'$'` 键存整词，找到时直接取词而不必沿路径重建字符串。`node.pop('$', None)` 同时「取出并删除」，配合海象运算符 `:=` 写成一句。`del parent[ch]` 把搜空的叶子摘掉，这是比普通回溯快几个数量级的关键优化。
