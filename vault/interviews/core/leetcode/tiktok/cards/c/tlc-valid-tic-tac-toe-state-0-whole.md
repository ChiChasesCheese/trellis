---
id: tlc-valid-tic-tac-toe-state-0-whole
node: c.valid-tic-tac-toe-state
type: qa
---
## Q
**LC 794 有效的井字游戏**｜Medium · LC TikTok 全时段热度 25/100

给你一个字符串数组 `board` 表示井字游戏的棋盘。当且仅当在井字游戏过程中，棋盘有可能达到 `board` 所显示的状态时，才返回 `true`。棋盘是 `3 x 3`，由字符 `' '`（空位）、`'X'`、`'O'` 组成。规则：玩家轮流把字符放入空位，玩家 1 总是放 `'X'`，玩家 2 总是放 `'O'`；只能放在空位里；当有 3 个相同（且非空）的字符填满任何行、列或对角线时，游戏结束；所有位置非空时也算游戏结束；游戏结束后不允许再放。`board.length == 3`，`board[i].length == 3`，`board[i][j]` 为 `'X'`、`'O'` 或 `' '`。例：`["O  ","   ","   "]` → `false`（玩家 1 先放 `X`）；`["XOX"," X ","   "]` → `false`（没有轮流）；`["XOX","O O","XOX"]` → `true`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 只检查三条必要且充分的条件：`X` 的个数是 `O` 的个数或多 1；`X` 赢则 `X` 必须刚好多 1；`O` 赢则两者必须一样多（同时赢必然矛盾）。

**识别。** 「判断一个状态是否可达」，状态空间极小（`3^9`），但不用搜索：从游戏规则推出不变量（先手比后手多 0 或 1 子，赢的一方一定是最后落子的一方），逐条验证。

**推导。** 先手 `X` 先落子，所以 `O <= X <= O + 1`，否则一定不可达。若 `X` 已连成一线，游戏在 `X` 落子的那一刻结束，所以 `X` 刚落完子：`X == O + 1`；若 `O` 连成一线，`O` 刚落完子：`X == O`。`X`、`O` 同时连线时，两个条件互相矛盾，自然返回 `False`。除此之外，不可能有别的非法情形：满足这三条的盘面总能构造出一个合法的落子顺序。

```python
def valid_tic_tac_toe(board: list[str]) -> bool:
    x = sum(row.count("X") for row in board)
    o = sum(row.count("O") for row in board)
    if not (o <= x <= o + 1):
        return False                             # 先手 X 比后手 O 多 0 或 1 子

    lines = [list(row) for row in board]                              # 3 行
    lines += [list(col) for col in zip(*board)]                       # 3 列
    lines += [[board[i][i] for i in range(3)], [board[i][2 - i] for i in range(3)]]   # 2 条对角线

    def wins(p: str) -> bool:
        return any(line == [p, p, p] for line in lines)

    if wins("X") and x != o + 1:
        return False                             # X 赢了：游戏在 X 落子时结束，X 必须刚好多 1 子
    if wins("O") and x != o:
        return False                             # O 赢了：游戏在 O 落子时结束，两者必须一样多
    return True                                  # X、O 同时赢时上面两条不可能同时通过
```

运行：`["O  ","   ","   "]` → `False`，`["XOX"," X ","   "]` → `False`，`["XOX","O O","XOX"]` → `True`；`["XXX","OO ","   "]` → `True`，`["XXX","OOO","   "]` → `False`，`["XXX","OO ","O  "]` → `False`，`["   ","   ","   "]` → `True`。

**复杂度。** 时间 `O(1)`（棋盘大小固定），空间 `O(1)`。

**拓展优化。**
- 推广到 `n x n` 棋盘、连成 `n` 个获胜：把 8 条线换成 `2n + 2` 条线，数量条件不变。

**易错点。**
- 只检查数量：`["XXX","OOO","   "]` 数量相等，得到 `True`，正确是 `False`（两方不可能同时赢）。
- `X` 赢了却只要求 `x >= o`：`["XXX","OO ","O  "]` 数量 `3 : 3`，得到 `True`，正确是 `False`（`X` 赢后 `O` 还在落子）。
- 把「赢的一方」判断成最后一个落子的一方时漏掉 `O` 赢的情形：`O` 赢时必须 `x == o`，而不是 `x == o + 1`。

**追问。**
- 判断某一步之后的胜负（LC 1275）：落子后只检查这一步所在的行、列、对角线。
- 给出一种具体的落子顺序：按 `X`、`O` 交替回放，把赢的一方留到最后落子。

**同模式。** LC 1275 找出井字棋的获胜者、LC 348 设计井字棋、LC 36 有效的数独、LC 37 解数独、LC 289 生命游戏。
