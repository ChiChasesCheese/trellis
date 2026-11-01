---
id: tlc-valid-tic-tac-toe-state-4-followup
node: p3.valid-tic-tac-toe-state
type: qa
step: 4
---
## Q
**LC 794 有效的井字游戏**｜追问

有效井字棋判断已经用「子数加连线」三条条件做到 `O(1)`。面试官接着问：（1）改成 `n x n` 棋盘、连成 `n` 个获胜？（2）不只判断，还要给出一种具体的落子顺序？（3）落完一步之后怎么快速判断这一步是否赢了？

## A
1. **`n x n`**：把 `3` 条行、`3` 条列、`2` 条对角线换成 `n + n + 2` 条线，子数条件不变。多出来一条要查：赢的一方必须存在一个「最后落下的子」，去掉它之后这一方不再连线，否则就是两条互不相交的线同属一方，无法在最后一步同时形成。`3 x 3` 里两条平行线要 `6` 个同色子，子数条件已经拦下，所以三条判断足够。
2. **构造落子顺序**：先排除非法盘面；若某方连线，取它所有获胜线的公共格子（一条线时是线上任一格，两条线时是交点）作为最后一子；其余的子按 `X, O, X, ...` 交替回放，最后落下这个子即可。
3. **每步判断胜负**：落子点只在一行、一列和至多两条对角线上，只检查这几条线，`O(1)`；或者像 LC 348 那样给每条线存一个带符号的计数，落子时加减 `1`，绝对值达到 `n` 即获胜。

```python
def won_after_move(board: list[list[str]], r: int, c: int) -> bool:
    p, n = board[r][c], len(board)
    return (all(board[r][j] == p for j in range(n))               # 落子所在行
            or all(board[i][c] == p for i in range(n))            # 落子所在列
            or (r == c and all(board[i][i] == p for i in range(n)))              # 主对角线
            or (r + c == n - 1 and all(board[i][n - 1 - i] == p for i in range(n))))   # 副对角线
```

**Python 提醒**：棋盘用 `list[list[str]]` 时初始化必须 `[[" "] * n for _ in range(n)]`，`[[" "] * n] * n` 的每一行是同一个对象，改一格会同时改一整列。
