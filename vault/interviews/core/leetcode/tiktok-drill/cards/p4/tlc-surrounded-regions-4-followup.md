---
id: tlc-surrounded-regions-4-followup
node: p4.surrounded-regions
type: qa
step: 4
---
## Q
**LC 130 被围绕的区域**｜追问

被围绕的区域已经用「从边缘的 `'O'` 出发递归 DFS，标成 `'#'`」解决。面试官接着问：（1）棋盘不能用临时字符（只读，或者字符集固定）怎么办？（2）能用并查集吗？（3）8 方向相连？（4）只统计有多少个被围绕的区域？（5）棋盘很大，递归爆栈怎么办？

## A
1. **不能用临时字符**：另开一个 `visited` 集合或二维布尔数组，从边缘的 `'O'` 出发搜索标记；最后把「是 `'O'` 且不在 `visited` 里」的格子写成 `'X'`。额外空间 `O(m·n)`。
2. **并查集**：多开一个虚拟节点 `edge`，每个边缘的 `'O'` 与它合并；每个 `'O'` 与上、左相邻的 `'O'` 合并；最后不与 `edge` 连通的 `'O'` 改成 `'X'`。时间近似 `O(m·n·α)`，代码比 BFS 长，但适合“不断添加格子、反复询问”的在线场景。
3. **8 方向**：把方向列表换成八个，其余不变；注意边缘上相邻的 `'O'` 在 8 方向下可能把更多区域连到边缘。
4. **统计被围绕的区域数**：先完成「标 `'#'`」的步骤，再对剩下的 `'O'` 做一遍岛屿计数（LC 200 的写法），每找到一个连通块计数加一。
5. **递归爆栈**：`200 x 200` 全 `'O'` 的递归深度可达 `4 * 10^4`，超过默认的约 1000。可以 `sys.setrecursionlimit`，或改成 BFS：从边缘的 `'O'` 入队，入队时就标记 `'#'`，同一格不会入队两次，不受递归上限影响：

```python
from collections import deque
from itertools import chain


def solve_bfs(board: list[list[str]]) -> None:
    m, n = len(board), len(board[0])
    border = chain(((r, c) for r in range(m) for c in (0, n - 1)),
                   ((r, c) for c in range(n) for r in (0, m - 1)))
    queue = deque()
    for r, c in border:
        if board[r][c] == "O":
            board[r][c] = "#"                    # 与边界相连的 O 先标成 #，入队时标记避免重复
            queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < m and 0 <= nc < n and board[nr][nc] == "O":
                board[nr][nc] = "#"
                queue.append((nr, nc))
    for r in range(m):
        for c in range(n):
            board[r][c] = "O" if board[r][c] == "#" else "X"   # # 还原成 O，剩下的 O 都是被围的，一起变 X
```


**Python 提醒**：`board[r][c] = ...` 能原地改是因为每一行是一个可变的 `list`；如果题目给的是字符串列表（`["XXX", ...]`），字符串不可变，要先转成 `list[list[str]]` 再改。二维数组初始化一律用 `[[...] * n for _ in range(m)]`，不要用 `[[...] * n] * m`，否则所有行是同一个对象。
