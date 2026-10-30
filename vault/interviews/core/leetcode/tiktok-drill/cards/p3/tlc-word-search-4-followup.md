---
id: tlc-word-search-4-followup
node: p3.word-search
type: qa
step: 4
---
## Q
**LC 79 单词搜索**｜追问

面试官接着问：（1）一次要在网格里找一整个单词表（LC 212），逐个单词搜索太慢怎么办？（2）输入棋盘不允许修改呢？（3）还有哪些剪枝能让更大的棋盘跑得快？

## A
1. **多个单词，用前缀树（Trie）**：把所有单词建成一棵树，DFS 沿着树往下走，棋盘上的路径只要在树里没有对应的前缀就立即停止；一次遍历同时匹配所有单词。找到单词后把它从树里取走，避免重复收集。

```python
def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    trie: dict = {}
    for w in words:
        node = trie
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = w                              # 在单词末尾存整个单词
    rows, cols, found = len(board), len(board[0]), []

    def dfs(r: int, c: int, node: dict) -> None:
        ch = board[r][c]
        nxt = node.get(ch)
        if nxt is None:
            return
        if "$" in nxt:
            found.append(nxt.pop("$"))             # 取走，避免重复收集
        board[r][c] = "#"
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != "#":
                dfs(nr, nc, nxt)
        board[r][c] = ch

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, trie)
    return found
```

`find_words` 在 `[["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]` 上找 `["oath","pea","eat","rain"]`，得到 `eat` 和 `oath`（顺序不定）。
2. **不允许修改棋盘**：用 `visited` 集合记录当前路径上的格子，进入前加入、返回前移除，判断多一项 `(nr, nc) not in visited`。空间 `O(L)`，每次集合操作 `O(1)`，只是常数比原地标记大一点。
3. **更多剪枝**：先统计字母数量（如主解法）；从出现次数少的一端开始；DFS 里提前检查剩余步数是否够用；多单词时，叶子节点处理完后从树里删掉空分支，避免反复进入已经没有单词的子树。

**Python 提醒**：递归函数里的 `any(...)` 接生成器，找到第一个 `True` 就停止，但回溯还原必须写在 `any` 之后、`return` 之前，不能放在 `any` 内部的短路路径上，否则提前返回会漏掉还原。
