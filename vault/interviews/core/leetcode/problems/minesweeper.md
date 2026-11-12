---
slug: minesweeper
---
## Q
**LC 529 扫雷游戏**｜Medium

扫雷盘面 `board`：`'M'` 未挖地雷，`'E'` 未挖空格，`'B'` 已挖空白，数字为相邻地雷数。给出一次点击 `click`，按规则返回点击后的盘面。

## A
**一句话。** 点到雷改 `'X'`；否则 DFS：周围 8 格有雷就写数字并停下，没有就写 `'B'` 并向周围的 `'E'` 展开。

```python
def updateBoard(board, click):
    m, n = len(board), len(board[0])
    dirs = [(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1)
            if a or b]                    # 8 个方向
    r0, c0 = click
    if board[r0][c0] == "M":
        board[r0][c0] = "X"
        return board

    def dfs(r, c):
        near = [(r + a, c + b) for a, b in dirs
                if 0 <= r + a < m and 0 <= c + b < n]
        mines = sum(board[x][y] == "M" for x, y in near)
        if mines:
            board[r][c] = str(mines)      # 有雷相邻：不再扩散
            return
        board[r][c] = "B"                 # 先标记再扩散
        for x, y in near:
            if board[x][y] == "E":
                dfs(x, y)

    dfs(r0, c0)
    return board
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 只数上下左右 4 个邻居：示例 1 第一行得 `["B","B","1","B","B"]`，应为 `["B","1","E","1","B"]`。
- 数字格也继续扩散：把地雷旁边的 `E` 也揭开了。
- `50 x 50` 全空时递归深度可达 2500，超过 CPython 默认上限，要调高或改 BFS。

**追问。**
- 玩家可插旗 `'F'`？：展开时遇到旗子不揭开。
- 统计这次点击揭开了多少格？：在写入 `'B'` 或数字时计数。

**同模式。** LC 200 岛屿数量、LC 733 图像渲染、LC 130 被围绕的区域、LC 1091 二进制矩阵中的最短路径
