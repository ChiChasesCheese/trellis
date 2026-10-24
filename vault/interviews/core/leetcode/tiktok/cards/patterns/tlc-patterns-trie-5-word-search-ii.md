---
id: tlc-patterns-trie-5-word-search-ii
node: patterns.trie
type: qa
step: 5
---
## Q
**字典树（Trie）｜单词搜索 II（LC 212）：字典树 + 回溯 + 剪枝**

网格里一次找几万个单词，为什么对每个单词各做一次回溯会超时？字典树怎样让搜索共享前缀、并及时剪枝？

## A
对 `3 * 10^4` 个单词逐个做回溯，每次最坏 `O(mn · 3^L)`，总量太大。把所有单词放进一棵字典树，**一次** DFS 同时尝试所有单词：从棋盘某格出发，沿着字典树的对应分支走，走不下去就剪掉。

```python
def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    root: dict = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = w                      # 单词结束处直接存下整个单词
    m, n = len(board), len(board[0])
    res: list[str] = []
    def dfs(r: int, c: int, parent: dict) -> None:
        ch = board[r][c]
        node = parent[ch]
        if "$" in node:
            res.append(node.pop("$"))      # 找到后删除标记，避免重复收集
        board[r][c] = "#"                  # 标记已用
        for a, b in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= a < m and 0 <= b < n and board[a][b] in node:
                dfs(a, b, node)
        board[r][c] = ch                   # 撤销
        if not node:
            del parent[ch]                 # 剪枝：这条分支的单词都找完了，从字典树里删掉
    for r in range(m):
        for c in range(n):
            if board[r][c] in root:
                dfs(r, c, root)
    return res
B = [list("oaan"), list("etae"), list("ihkr"), list("iflv")]
print(sorted(find_words(B, ["oath", "pea", "eat", "rain"])), find_words([list("ab"), list("cd")], ["abcb"]))   # ['eat', 'oath'] []
```

- **单词存在结束标记里**：不用在回溯中再拼接字符串。
- **删除已找到的单词**避免同一个单词被多条路径重复加入；**删除空节点**使后续搜索越来越快。
- 一个 `12 x 12` 的棋盘和 `3 * 10^4` 个随机单词，这个写法在 Python 中几秒内完成。
- 棋盘格被标记为 `"#"`，要确保 `"#"` 不是字典树的合法字符（单词只含小写字母）。
