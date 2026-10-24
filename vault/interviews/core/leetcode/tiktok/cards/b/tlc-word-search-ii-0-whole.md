---
id: tlc-word-search-ii-0-whole
node: b.word-search-ii
type: qa
---
## Q
**LC 212 单词搜索 II**｜Hard · TikTok 高频

给一个 `m x n` 的字符网格 `board` 和一个单词列表 `words`，返回所有能在网格上找到的单词。单词必须按字母顺序，由**相邻**（水平或竖直）的格子构成；同一个格子在同一个单词里不能重复使用。`m == board.length`，`n == board[i].length`，`1 <= m, n <= 12`，`board[i][j]` 是小写字母，`1 <= words.length <= 3 * 10^4`，`1 <= words[i].length <= 10`，`words[i]` 由小写字母组成，`words` 中的字符串互不相同。例：`board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]`，`words = ["oath","pea","eat","rain"]` → `["eat","oath"]`；`board = [["a","b"],["c","d"]]`，`words = ["abcb"]` → `[]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 把所有单词建成字典树（trie），然后从网格的每个格子出发做深度优先搜索（DFS）回溯，**沿字典树同步下行**：只有当下一个字符在当前字典树结点的孩子里才继续走，走到存有整词的结点就收集；搜到的词从树里摘掉、搜空的分支剪掉。

**识别。** 「多个单词在网格里找」是 LC 79（单个单词）的升级：逐词搜索会把同一批路径重复走很多遍。单词很多（`3 * 10^4`）而且有大量公共前缀 → 字典树把所有单词合并成一棵树，一次 DFS 同时对应所有单词；「网格 + 路径不能重复经过同一格 + 回溯」是 DFS 回溯的固定写法。`m, n <= 12`、单词长度 `<= 10`，递归深度不超过 `10`。

**推导。** 暴力：对每个单词都做一次 LC 79，复杂度 `O(W · mn · 3^L)`，`W = 3 * 10^4` 个词会超时。浪费：`"oath"` 和 `"oat"` 的前三步完全一样，却分别搜了两遍；某个前缀在网格里根本走不通时，所有以它为前缀的单词都白搜了。洞察：把单词建成字典树，DFS 的每一步同时前进「网格位置」和「字典树结点」；当前结点没有对应的孩子就立刻回头，等于一次剪掉所有以该前缀开头的单词。再加两个优化：找到的单词从结点上摘掉（不会重复收集），叶子结点搜空后从父亲上删除（以后不再进入）。

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

运行：示例 1 → `['eat', 'oath']`，示例 2 → `[]`，`[["a"]]` 找 `["a"]` → `['a']`，`[["a","a"]]` 找 `["a"]` → `['a']`；`12 x 12` 随机 `a/b/c` 盘面、`30000` 个长 `5..10` 的不同单词 → 找到 `28153` 个，约 `40 ms`；全 `a` 的 `12 x 12` 盘面、单词 `"a"` 到 `"a" * 10` → `10` 个，瞬间完成。

**复杂度。** 时间最坏 `O(mn · 3^L)`（`L` 为最长单词，每格出发最多沿 `4 → 3` 个方向走 `L` 步），字典树剪枝后远小于它；空间 `O(总字符数)` 存字典树，加递归深度 `O(L)`。

**易错点。**
- 找到单词不摘掉：`board = [["a","a"]]`、`words = ["a"]`，从两个格子各找到一次，返回 `['a', 'a']`，正确是 `['a']`。
- 不剪空分支：全 `a` 的 `12 x 12` 盘面、单词 `"a"` 到 `"a" * 10`，单词早就找全了，不剪枝还要把剩下的路径全部走一遍，耗时 `0.364 s`，剪掉则几乎为 `0`。
- 回溯时忘了还原格子（`board[i][j] = ch`）：后续起点看到的盘面被破坏，漏掉单词。

**追问。**
- 单个单词（LC 79）：直接 DFS 回溯，不用字典树。
- 同一个格子可以重复使用：去掉 `#` 占位和回溯还原，但要给搜索加深度上限（单词长度），否则无限循环。
- 需要每个单词的路径：把当前路径作为栈传下去，在摘词时一并保存。

**同模式。** LC 79 单词搜索、LC 208 实现 Trie、LC 140 单词拆分 II、LC 472 连接词、LC 676 实现一个魔法字典。
