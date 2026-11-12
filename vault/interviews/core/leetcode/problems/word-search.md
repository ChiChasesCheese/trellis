---
slug: word-search
---
## Q
**LC 79 单词搜索**｜Medium

给 `m x n` 的字符网格 `board` 和字符串 `word`，判断 `word` 是否存在于网格中。单词必须按字母顺序，通过水平或竖直相邻的单元格连成；**同一个单元格内的字母在一条路径里不能重复使用**。`m == board.length`，`n == board[i].length`，`1 <= m, n <= 6`，`1 <= word.length <= 15`，`board` 和 `word` 仅由大小写英文字母组成。进阶：能否用搜索剪枝让更大的 `board` 也跑得快？例：`board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]`，`word = "ABCCED"` → `true`；`"SEE"` → `true`；`"ABCB"` → `false`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 回溯（DFS）：对每个格子作为起点，沿四个方向逐字符匹配；走过的格子临时改成 `"#"` 标记为本条路径已用，回溯时还原。再加两个剪枝：棋盘上某个字母的数量不够就直接 `False`；从出现次数更少的一端开始匹配。

**识别。** 「网格里按相邻关系拼出一个序列」「不能重复用同一格」是网格回溯（grid backtracking）的信号，与数岛屿不同：这里要的是**路径**，同一个格子在不同路径里可以重复访问，所以走完要还原标记。`m, n <= 6`、`word.length <= 15`，最坏分支 `3` 个（不能回头），`6 * 6 * 3^14` 量级可接受，加剪枝更稳。

**推导。** 暴力：枚举所有路径。优化 1：只从与 `word[0]` 相同的格子开始，字符不匹配立刻返回，搜索被"字符必须匹配"天然剪枝。优化 2：标记已用格子，避免重复使用同一格。优化 3（进阶）：`word` 比棋盘字母多就不可能；`word` 首尾字母在棋盘上的数量不同，从少的一端开始更省分支（首字母多的话反转单词）。

**简单解法。** 朴素回溯：每个格子当起点，`visited` 集合记本条路径用过的格子，不做任何字母计数或反转的剪枝。

```python
def exist(board: list[list[str]], word: str) -> bool:
    rows, cols = len(board), len(board[0])
    # 本条路径已用过的格子，不改输入
    visited: set[tuple[int, int]] = set()

    # 站在 (r, c)，要匹配 word[k]
    def dfs(r: int, c: int, k: int) -> bool:
        if board[r][c] != word[k]:
            return False
        if k == len(word) - 1:
            return True
        visited.add((r, c))
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if (0 <= nr < rows and 0 <= nc < cols
                    and (nr, nc) not in visited
                    and dfs(nr, nc, k + 1)):
                visited.discard((r, c))
                return True
        # 回溯：这格在别的路径里还能用
        visited.discard((r, c))
        return False

    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))
```

时间最坏 `O(mn * 3^L)`，空间 `O(L)`；`6 x 6`、`L <= 15` 的约束内够用，开场答案；棋盘更大或单词全是重复字母时才需要主解的两个剪枝。

最优解：

```python
from collections import Counter
from itertools import chain


def exist(board: list[list[str]], word: str) -> bool:
    rows, cols = len(board), len(board[0])
    board_count = Counter(chain.from_iterable(board))
    # 单词需要的某个字母比棋盘上的还多：直接 False
    if Counter(word) - board_count:
        return False
    if board_count[word[0]] > board_count[word[-1]]:
        # 从出现次数少的一端起手，起点更少
        word = word[::-1]

    # 当前站在 (r, c)，要匹配 word[k]
    def dfs(r: int, c: int, k: int) -> bool:
        if board[r][c] != word[k]:
            return False
        if k == len(word) - 1:
            return True
        # 原地标记"本条路径已用过"
        board[r][c] = "#"
        found = any(
            0 <= nr < rows and 0 <= nc < cols
            and dfs(nr, nc, k + 1)
            for nr, nc in ((r + 1, c), (r - 1, c),
                           (r, c + 1), (r, c - 1))
        )
        board[r][c] = word[k]                      # 回溯：还原
        return found

    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))
```

运行：`ABCCED` → `True`，`SEE` → `True`，`ABCB` → `False`；`[["a"]], "a"` → `True`；`[["a"]], "b"` → `False`；`[["a","a"]], "aaa"` → `False`；调用后 `board` 保持原样。

**复杂度。** 时间最坏 `O(mn * 3^L)`，`L` 是单词长度（首步 4 个方向，之后不能回头，至多 3 个）；空间 `O(L)`（递归栈）。

**拓展优化。**
- 一次找多个单词（LC 212）：把单词建成前缀树（Trie），一次 DFS 同时匹配所有单词；找到就把单词取走，空枝剪掉：
```python
from typing import Any


def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    trie: dict[str, Any] = {}
    for w in words:
        node = trie
        for ch in w:
            node = node.setdefault(ch, {})
        # 单词结尾处存下整个单词
        node["$"] = w
    rows, cols = len(board), len(board[0])
    found: list[str] = []

    def dfs(r: int, c: int, parent: dict[str, Any]) -> None:
        ch = board[r][c]
        node = parent.get(ch)
        if node is None:
            # 前缀树里没有这条路：剪枝
            return
        if "$" in node:
            # 取走，同一个单词不会重复收集
            found.append(node.pop("$"))
        board[r][c] = "#"                           # 本条路径已用
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if (0 <= nr < rows and 0 <= nc < cols
                    and board[nr][nc] != "#"):
                dfs(nr, nc, node)
        board[r][c] = ch                            # 回溯
        if not node:
            # 子树已空：剪掉，后面不再进入
            parent.pop(ch)

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, trie)
    return found
```

**易错点。**
- 不标记已用的格子：`[["a","b"]]` 找 `"aba"` 会得到 `True`（`a` 被用了两次），正确是 `False`。
- 回溯时漏掉还原：失败路径留下的 `"#"` 会阻断之后的起点，`[["a","a","b","b"]]` 找 `"bba"`：先从下标 `2` 的 `b` 起走，走进下标 `3` 的 `b` 失败，两格都留着 `"#"`，最终得到 `False`，正确是 `True`（下标 `3 → 2 → 1`）。
- `any(...)` 的生成器里先判断坐标范围再递归，否则越界下标会抛 `IndexError`；负下标不会报错，但会读到另一侧的格子，必须显式检查 `0 <= nr`。

**追问。**
- 返回具体路径：`dfs` 成功返回时（`True` 一路向上传）顺便把坐标 `append` 进列表，最后反转。
- 允许八个方向：方向元组换成八个。
- 为什么要反转单词、先数字母？`6 x 6` 全是 `"a"` 的棋盘找 `"aaaaaaaaaaaaaab"`（`14` 个 `a` 再一个 `b`）：不剪枝要把指数级的 `a` 路径全试完才失败（秒级），字母计数一步就返回 `False`。
- 多个单词怎么办？每个单词跑一遍是 `O(单词数 * mn * 3^L)`；用拓展优化里的前缀树，一次 DFS 同时匹配所有单词，共享前缀只搜一次。

**同模式。** LC 212 单词搜索 II、LC 51 N 皇后、LC 130 被围绕的区域、LC 200 岛屿数量、LC 980 不同路径 III。
