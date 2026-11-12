---
slug: game-of-life
---
## Q
**LC 289 生命游戏**｜Medium

`board` 中 `1` 活 `0` 死，按生命游戏规则（八邻居，同时更新）原地更新到下一状态。

## A
**一句话。** 先拷贝旧面板，所有邻居计数都读旧面板，新状态写回 `board`。

```python
def game_of_life(board):
    m, n = len(board), len(board[0])
    old = [row[:] for row in board]     # 快照，保证"同时"更新
    for i in range(m):
        for j in range(n):
            # 夹到边界内的 3x3 窗口，减去自己 = 邻居活数
            xs = range(max(0, i - 1), min(m, i + 2))
            ys = range(max(0, j - 1), min(n, j + 2))
            live = sum(old[x][y] for x in xs for y in ys)
            live -= old[i][j]
            # 邻居 3 个必活；2 个保持原状
            board[i][j] = int(live == 3 or
                              old[i][j] and live == 2)
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 边算边改原面板：后面的格子读到新状态，结果错乱。
- 邻居计数忘了减 `old[i][j]`：自己被算进邻居。
- 负下标绕回：`board[-1]` 不报错，面板被当成环面。

**追问。**
- 怎么做到 `O(1)` 空间？：用两位编码，`2` 表示活变死，`3` 表示死变活，读时对 `% 2` 取旧状态，最后统一还原。
- 面板无限大怎么办？：只存活细胞坐标的集合，每步统计其邻居的计数。

**同模式。** LC 73 矩阵置零、LC 54 螺旋矩阵、LC 48 旋转图像、LC 36 有效的数独
