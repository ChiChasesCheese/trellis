---
slug: word-search-ii
---
## Q
**LC 212 单词搜索 II**｜Hard

在字符网格里找出 `words` 中所有能沿相邻格子（上下左右、同格不重复用）拼出的单词。

## A
**一句话。** 单词建字典树，从每格出发 DFS 回溯并沿字典树同步下行，到整词就收集，搜完的词和空分支都摘掉。

```python
def find_words(board, words):
    root = {}                    # 字典树，'$' 存整词
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node['$'] = w
    m, n = len(board), len(board[0])
    found = []
    def dfs(i, j, parent):
        ch = board[i][j]
        node = parent[ch]
        if w := node.pop('$', None):     # 摘词，不会找到两次
            found.append(w)
        board[i][j] = '#'                # 本路径内不重复用
        for x, y in (i+1, j), (i-1, j), (i, j+1), (i, j-1):
            if (0 <= x < m and 0 <= y < n
                    and board[x][y] in node):
                dfs(x, y, node)
        board[i][j] = ch                 # 回溯
        if not node:
            del parent[ch]               # 剪掉搜空的分支
    for i in range(m):
        for j in range(n):
            if board[i][j] in root:
                dfs(i, j, root)
    return found
```

**复杂度。** 时间最坏 `O(mn·3^L)`，空间 `O(总字符数)`。

**易错点。**
- 找到单词不摘掉：`[["a","a"]]`、`["a"]` 返回 `['a','a']`。
- 不剪空分支：全 `a` 的盘面上找全后仍白白走完剩余路径。
- 回溯忘了还原格子：后续起点看到被破坏的盘面，漏词。

**追问。**
- 只找单个单词（LC 79）？：直接 DFS 回溯，不用字典树。
- 同一格可重复使用？：去掉占位与还原，但要用单词长度限制深度。

**同模式。** LC 79 单词搜索、LC 208 实现 Trie、LC 140 单词拆分 II、LC 472 连接词
