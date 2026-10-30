---
id: tlc-core-word-search
node: p3.word-search
type: qa
---
## Q
**LC 79 单词搜索**｜Medium · LC TikTok 热度 75/100（近 6 个月） · CodeTop 国内累计 41 次 · 最近 2026-06-03（国内 CodeTop） · 也在：Amazon、LeetCode Hot 100、Blind 75、NeetCode 150、Top Interview 150

给 `m x n` 的字符网格 `board` 和字符串 `word`，判断 `word` 是否存在于网格中。单词必须按字母顺序，通过水平或竖直相邻的单元格连成；**同一个单元格内的字母在一条路径里不能重复使用**。`m == board.length`，`n == board[i].length`，`1 <= m, n <= 6`，`1 <= word.length <= 15`，`board` 和 `word` 仅由大小写英文字母组成。进阶：能否用搜索剪枝让更大的 `board` 也跑得快？例：`board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]`，`word = "ABCCED"` → `true`；`"SEE"` → `true`；`"ABCB"` → `false`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 回溯（DFS）：对每个格子作为起点，沿四个方向逐字符匹配；走过的格子临时改成 `"#"` 标记为本条路径已用，回溯时还原。再加两个剪枝：棋盘上某个字母的数量不够就直接 `False`；从出现次数更少的一端开始匹配。

**识别。** 「网格里按相邻关系拼出一个序列」「不能重复用同一格」是网格回溯（grid backtracking）的信号，与数岛屿不同：这里要的是**路径**，同一个格子在不同路径里可以重复访问，所以走完要还原标记。`m, n <= 6`、`word.length <= 15`，最坏分支 `3` 个（不能回头），`6 * 6 * 3^14` 量级可接受，加剪枝更稳。

**推导。** 暴力：枚举所有路径。优化 1：只从与 `word[0]` 相同的格子开始，字符不匹配立刻返回，搜索被"字符必须匹配"天然剪枝。优化 2：标记已用格子，避免重复使用同一格。优化 3（进阶）：`word` 比棋盘字母多就不可能；`word` 首尾字母在棋盘上的数量不同，从少的一端开始更省分支（首字母多的话反转单词）。

```python
from collections import Counter
from itertools import chain


def exist(board: list[list[str]], word: str) -> bool:
    rows, cols = len(board), len(board[0])
    board_count = Counter(chain.from_iterable(board))
    if Counter(word) - board_count:                # 单词需要的某个字母比棋盘上的还多：直接 False
        return False
    if board_count[word[0]] > board_count[word[-1]]:
        word = word[::-1]                          # 从出现次数少的一端起手，起点更少

    def dfs(r: int, c: int, k: int) -> bool:       # 当前站在 (r, c)，要匹配 word[k]
        if board[r][c] != word[k]:
            return False
        if k == len(word) - 1:
            return True
        board[r][c] = "#"                          # 原地标记"本条路径已用过"
        found = any(
            0 <= nr < rows and 0 <= nc < cols and dfs(nr, nc, k + 1)
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1))
        )
        board[r][c] = word[k]                      # 回溯：还原
        return found

    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))
```

运行：`ABCCED` → `True`，`SEE` → `True`，`ABCB` → `False`；`[["a"]], "a"` → `True`；`[["a"]], "b"` → `False`；`[["a","a"]], "aaa"` → `False`；调用后 `board` 保持原样。

**复杂度。** 时间最坏 `O(mn * 3^L)`，`L` 是单词长度（首步 4 个方向，之后不能回头，至多 3 个）；空间 `O(L)`（递归栈）。

**易错点。**
- 不标记已用的格子：`[["a","b"]]` 找 `"aba"` 会得到 `True`（`a` 被用了两次），正确是 `False`。
- 回溯时漏掉还原：失败路径留下的 `"#"` 会阻断之后的起点，`[["a","b","b"]]` 找 `"bba"` 会得到 `False`，正确是 `True`。
- `any(...)` 的生成器里先判断坐标范围再递归，否则越界下标会抛 `IndexError`；负下标不会报错，但会读到另一侧的格子，必须显式检查 `0 <= nr`。

**追问。**
- 一次找多个单词（LC 212）：把所有单词建成前缀树（Trie），一次 DFS 同时匹配多个单词，找到就把单词从树里取走。
- 不能修改输入：改用 `visited` 集合，路径结束后移除。
- 允许八个方向：方向元组换成八个。

**同模式。** LC 212 单词搜索 II、LC 51 N 皇后、LC 130 被围绕的区域、LC 200 岛屿数量、LC 980 不同路径 III。
