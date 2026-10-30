---
id: tlc-word-search-2-code
node: p3.word-search
type: qa
step: 2
---
## Q
**LC 79 单词搜索**｜写出 Python 实现

`board` 是 `m x n` 的字符网格（`1 <= m, n <= 6`），`word` 长度 `1 <= word.length <= 15`，都只含英文字母。判断 `word` 能否由水平或竖直相邻的格子按顺序拼出，同一格在一条路径里只能用一次。加上能让更大棋盘也跑得快的剪枝。

## A
**思路。** 先用计数做两个剪枝（字母数量不够直接 `False`；从出现次数更少的一端起手）。然后对每个起点做 DFS：当前格与 `word[k]` 不匹配就返回 `False`，匹配到最后一个字符就返回 `True`；否则把当前格改成 `"#"`，尝试四个方向，最后还原。

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

运行：示例 `"ABCCED"` → `True`，`"SEE"` → `True`，`"ABCB"` → `False`；`[["a"]], "a"` → `True`；`[["a"]], "b"` → `False`；`[["a","a"]], "aaa"` → `False`；每次调用后 `board` 内容不变。

**复杂度。** 时间最坏 `O(mn * 3^L)`（`L` 为单词长度）；空间 `O(L)`（递归深度 `L <= 15`）。

**写法要点。** `Counter(word) - board_count` 是多重集合的差，结果非空就说明单词需要的某个字母比棋盘多；`chain.from_iterable(board)` 把二维棋盘摊平，不建临时列表；`any(生成器)` 在找到第一个成功分支后立刻停止，且这时标记还没还原的格子只有当前这一个，后面的还原一定会执行；坐标范围检查放在 `dfs` 调用之前，利用 `and` 的短路；`word[::-1]` 反转单词，棋盘不变；还原写成 `word[k]` 而不是保存旧值，因为匹配成功时它就等于原字符。
