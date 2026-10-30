---
id: tlc-surrounded-regions-2-code
node: p4.surrounded-regions
type: qa
step: 2
---
## Q
**LC 130 被围绕的区域**｜写出 Python 实现

`board` 是 `m x n` 的字符矩阵（`1 <= m, n <= 200`），元素是 `'X'` 或 `'O'`。原地把所有被 `'X'` 围绕的 `'O'` 区域（区域内没有任何 `'O'` 在边缘）改成 `'X'`，无返回值。

## A
**思路。** 从四条边上的 `'O'` 出发 BFS，把相连的 `'O'` 标成 `'#'`；最后扫描整个棋盘，`'#'` 还原为 `'O'`，其余格子（剩下的 `'O'` 都是被围绕的）统一写成 `'X'`。

```python
from collections import deque
from itertools import chain


def solve(board: list[list[str]]) -> None:
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

运行：`[["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]` → `['XXXX', 'XXXX', 'XXXX', 'XOXX']`；`[["X"]]` → `[["X"]]`；`[["O"]]` → `[["O"]]`；`["XXX","OOX","XXX"]` → 不变；`200 x 200` 全 `'O'` → `40000` 个 `'O'` 全部保留；外圈 `'X'` 内部全 `'O'` → `0` 个 `'O'`。

**复杂度。** 时间 `O(m·n)`，空间 `O(m·n)`（队列）。

**写法要点。**
- `itertools.chain` 把「左右两列」「上下两行」两个生成器串成一个迭代器，边缘格子一次遍历；角上的格子会出现两次，但第二次已经是 `'#'`，不会重复入队。
- 入队前就改成 `'#'`：标记即访问，同一个格子不会入队两次；`'#'` 既是“已访问”也是“要保留”。
- 最后一遍扫描用条件表达式一行完成「`'#'` 还原为 `'O'`、其余写 `'X'`」，不需要判断原来是什么。
- `deque.popleft()` 是 `O(1)`；`list.pop(0)` 是 `O(n)`，不要拿列表当队列。
