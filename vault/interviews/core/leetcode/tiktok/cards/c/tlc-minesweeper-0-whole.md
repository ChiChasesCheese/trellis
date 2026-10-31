---
id: tlc-minesweeper-0-whole
node: c.minesweeper
type: qa
---
## Q
**LC 529 扫雷游戏**｜Medium · LC TikTok 全时段热度 26/100

给你一个 `m x n` 的字符矩阵 `board` 表示扫雷盘面：`'M'` 未挖出的地雷，`'E'` 未挖出的空方块，`'B'` 没有相邻（上下左右和 4 个对角线）地雷的已挖出空白方块，数字 `'1'` 到 `'8'` 表示相邻地雷数，`'X'` 已挖出的地雷。给你整数数组 `click = [clickr, clickc]`，表示在所有未挖出方块（`'M'` 或 `'E'`）中的下一个点击位置。按规则返回点击后的盘面：挖到地雷（`'M'`）改成 `'X'`，游戏结束；挖到没有相邻地雷的 `'E'` 改成 `'B'`，并递归揭开所有相邻的未挖出方块；挖到至少与一个地雷相邻的 `'E'` 改成数字；没有更多方块可揭开时返回盘面。`1 <= m, n <= 50`，`board[i][j]` 是 `'M'`、`'E'`、`'B'` 或 `'1'` 到 `'8'`，`board[clickr][clickc]` 是 `'M'` 或 `'E'`。例：`board = [["E","E","E","E","E"],["E","E","M","E","E"],["E","E","E","E","E"],["E","E","E","E","E"]], click = [3,0]` → `[["B","1","E","1","B"],["B","1","M","1","B"],["B","1","1","1","B"],["B","B","B","B","B"]]`；再点 `[1,2]`（地雷）得到该位置变成 `"X"`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 点到地雷直接改成 `'X'` 结束；否则对点击格做 DFS：数周围 8 格的地雷数，有地雷就写数字并停下，没有就写 `'B'` 并继续向周围未挖出的 `'E'` 展开，`O(mn)`。

**识别。** 「点一下，连带展开一片」是网格上的洪水填充（flood fill），和「岛屿数量」同一类。只有「周围 0 雷」的格子才继续扩散，数字格是边界。

**推导。** 每个格子最多被揭开一次：揭开时立刻把它从 `'E'` 改成 `'B'` 或数字，后面再遇到就不是 `'E'`，不会重复进入。每个格子检查 8 个邻居，总计 `O(8mn)`。

```python
def update_board(board: list[list[str]], click: list[int]) -> list[list[str]]:
    rows, cols = len(board), len(board[0])
    dirs = [(dr, dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1) if dr or dc]   # 8 个方向
    r0, c0 = click
    if board[r0][c0] == "M":
        board[r0][c0] = "X"                      # 踩雷：游戏结束
        return board

    def dfs(r: int, c: int) -> None:
        mines = sum(0 <= r + dr < rows and 0 <= c + dc < cols and board[r + dr][c + dc] == "M"
                    for dr, dc in dirs)          # 周围 8 格的地雷数
        if mines:
            board[r][c] = str(mines)             # 有雷相邻：写数字，不再扩散
            return
        board[r][c] = "B"                        # 先标记再扩散，同一格不会被重复进入
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == "E":
                dfs(nr, nc)

    dfs(r0, c0)
    return board
```

运行：示例 1（点 `[3,0]`）→ `[["B","1","E","1","B"],["B","1","M","1","B"],["B","1","1","1","B"],["B","B","B","B","B"]]`；示例 2（点 `[1,2]`）→ 该格变 `"X"`，其余不变；`[["E"]]` 点 `[0,0]` → `[["B"]]`，`[["M"]]` 点 `[0,0]` → `[["X"]]`；`50 x 50` 全是 `"E"`、点 `[0,0]` → 全部 `"B"`（默认递归上限下抛 `RecursionError`，调到 `10000` 后正常）。

**复杂度。** 时间 `O(mn)`（每格揭开一次，检查常数个邻居），空间 `O(mn)`（递归栈最深可到格子总数）。

**拓展优化。**
- 递归深度超限时改用 BFS，揭开逻辑完全相同，入队时就标记。

```python
from collections import deque


def update_board_bfs(board: list[list[str]], click: list[int]) -> list[list[str]]:
    rows, cols = len(board), len(board[0])
    dirs = [(dr, dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1) if dr or dc]
    r0, c0 = click
    if board[r0][c0] == "M":
        board[r0][c0] = "X"
        return board
    queue = deque([(r0, c0)])
    seen = {(r0, c0)}                            # 入队即标记，避免同一格多次入队
    while queue:
        r, c = queue.popleft()
        mines = sum(0 <= r + dr < rows and 0 <= c + dc < cols and board[r + dr][c + dc] == "M"
                    for dr, dc in dirs)
        if mines:
            board[r][c] = str(mines)
            continue
        board[r][c] = "B"
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == "E" and (nr, nc) not in seen:
                seen.add((nr, nc))
                queue.append((nr, nc))
    return board
```

**易错点。**
- 只数上下左右 4 个邻居：示例 1 第一行得到 `["B","B","1","B","B"]`，正确是 `["B","1","E","1","B"]`。
- 数字格也继续扩散：示例 1 第一行得到 `["B","1","1","1","B"]`，把地雷上方的 `E` 也揭开了。
- 递归深度：`50 x 50` 全空时 DFS 最深可到 2500，CPython 默认上限约 1000，会抛 `RecursionError`，要调高上限或改 BFS。

**追问。**
- 玩家可以右键标记地雷（`'F'`）：展开时遇到旗子的格子不揭开。
- 输出这次点击揭开了多少格：在揭开时计数。

**同模式。** LC 200 岛屿数量、LC 733 图像渲染、LC 130 被围绕的区域、LC 417 太平洋大西洋水流问题、LC 1091 二进制矩阵中的最短路径。
