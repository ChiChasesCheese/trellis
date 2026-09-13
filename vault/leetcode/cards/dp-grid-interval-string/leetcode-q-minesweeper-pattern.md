---
id: leetcode-q-minesweeper-pattern
node: dp-grid-interval-string.matrix
type: qa
anki: 1787268625913
tags: [lc::529, leetcode, pattern, recall]
---
## Q
Minesweeper（扫雷）揭示格子的算法模型是什么？如何处理点击到雷、点击到空白格、点击到数字格三种情况？

## A
用 DFS/BFS 做八方向 flood fill：
1. 若点击格是 'M'（雷），直接标记为 'X'，结束。
2. 否则统计该格八个方向内相邻雷的数量 mines。
3. 若 mines > 0，标记为数字字符 str(mines)，不再向外扩展。
4. 若 mines == 0，标记为 'B'，并对八个方向中仍为 'E'（未揭示）的格子递归/入队继续处理。
关键不变量：只有 'B'（空白，周围无雷）的格子才继续向外扩散，数字格是扩散的边界，从而保证结果与规则一致且不会死循环。

**Evidence**

```
def dfs(i, j):
    if board[i][j] == "M":
        board[i][j] = "X"
        return
    mines = 0
    for i_off, j_off in directions:
        ...
    if mines > 0:
        board[i][j] = str(mines)
    else:
        board[i][j] = "B"
        for i_off, j_off in directions:
            ...
            if board[r][c] == "E":
                dfs(r, c)
```

[原文 ↗](obsidian://open?vault=lc&file=questions%2F529%20-%20Minesweeper)
