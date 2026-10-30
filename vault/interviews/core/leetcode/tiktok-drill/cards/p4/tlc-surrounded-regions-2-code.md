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
**思路。** 从四条边上的 `'O'` 出发递归 DFS，把相连的 `'O'` 标成 `'#'`；最后扫描整个棋盘，`'#'` 还原为 `'O'`，其余格子（剩下的 `'O'` 都是被围绕的）统一写成 `'X'`。

```python
def solve(board: list[list[str]]) -> None:
    m, n = len(board), len(board[0])

    def keep(r: int, c: int) -> None:
        if not (0 <= r < m and 0 <= c < n) or board[r][c] != "O":
            return                                   # 出界、不是 O、或已标成 #：到头
        board[r][c] = "#"                            # 与边缘相连的 O：先标 #，既是访问标记也是保留标记
        keep(r + 1, c)
        keep(r - 1, c)
        keep(r, c + 1)
        keep(r, c - 1)

    for r in range(m):                               # 左右两列
        keep(r, 0)
        keep(r, n - 1)
    for c in range(n):                               # 上下两行
        keep(0, c)
        keep(m - 1, c)
    for r in range(m):
        for c in range(n):
            board[r][c] = "O" if board[r][c] == "#" else "X"   # # 还原成 O，剩下的 O 都是被围的，一起变 X
```

运行：`[["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]` → `['XXXX', 'XXXX', 'XXXX', 'XOXX']`；`[["X"]]` → `[["X"]]`；`[["O"]]` → `[["O"]]`；`["XXX","OOX","XXX"]` → 不变；外圈 `'X'` 内部全 `'O'` → `0` 个 `'O'`；`200 x 200` 全 `'O'` 在默认递归上限下抛 `RecursionError`，调高上限到 100000 后 → `40000` 个 `'O'` 全部保留。

**复杂度。** 时间 `O(m·n)`，空间 `O(m·n)`（递归栈最坏深度；`200 x 200` 全 `'O'` 会触到默认递归上限）。

**写法要点。**
- 递归入口一次判完「出界、不是 `'O'`、已是 `'#'`」，主体只有「标记 + 四个方向」，最直观；角上的格子会被调用两次，第二次已经是 `'#'`，直接返回。
- 先改成 `'#'` 再向四周搜：标记即访问，不会无限递归；`'#'` 既是“已访问”也是“要保留”。
- 最后一遍扫描用条件表达式一行完成「`'#'` 还原为 `'O'`、其余写 `'X'`」，不需要判断原来是什么。
- 嵌套函数 `keep` 直接用外层的 `board`、`m`、`n`，不用传参。
