---
slug: surrounded-regions
---
## Q
**LC 130 被围绕的区域**｜Medium

`m x n` 的棋盘由 `'X'`、`'O'` 组成。把所有不与边缘 `'O'` 相连的 `'O'` 区域原地改成 `'X'`。

## A
**一句话。** 反着找：从边缘的 `'O'` 出发做 DFS 标成 `'#'`，最后 `'#'` 还原成 `'O'`，剩下的 `'O'` 全是被围的。

```python
def solve(board):
    m, n = len(board), len(board[0])

    def dfs(r, c):
        if 0 <= r < m and 0 <= c < n and board[r][c] == "O":
            board[r][c] = "#"        # 先标记，兼作 visited
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)

    for r in range(m):
        dfs(r, 0)
        dfs(r, n - 1)
    for c in range(n):
        dfs(0, c)
        dfs(m - 1, c)
    for r in range(m):
        for c in range(n):
            board[r][c] = "O" if board[r][c] == "#" else "X"
```

**复杂度。** 时间 `O(mn)`，空间 `O(mn)`。

**易错点。**
- 只改内部 `'O'`、不沿边缘搜索：`["XXX","OOX","XXX"]` 里 `(1,1)` 与边缘 `(1,0)` 相连，应保留，却被改成 `'X'`。
- 最后忘了还原 `'#'`：棋盘残留 `'#'`。
- 进入格子前不先标记：相邻两格互相调用，无限递归。

**追问。**
- `200 x 200` 全 `'O'` 递归会爆栈？：会，深度可达 `4*10^4`；改成 BFS，边缘 `'O'` 入队时就标 `'#'`。
- 不许改成临时字符？：另开 `visited` 集合，多 `O(mn)` 空间。
- 并查集怎么做？：加一个虚拟节点，边缘 `'O'` 与它合并，相邻 `'O'` 互相合并，不与虚拟节点连通的改 `'X'`。

**同模式。** LC 200 岛屿数量、LC 417 太平洋大西洋水流问题、LC 1020 飞地的数量、LC 1254 统计封闭岛屿的数目
