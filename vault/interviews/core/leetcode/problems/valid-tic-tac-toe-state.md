---
slug: valid-tic-tac-toe-state
---
## Q
**LC 794 有效的井字游戏**｜Medium

`3 x 3` 棋盘（`' '`、`'X'`、`'O'`），`X` 先手轮流落子，有人连成三个或棋盘满则结束，结束后不能再落。判断该棋盘是否可能在游戏中出现。例：`["XOX"," X ","   "]` → `false`。

## A
**一句话。** 只查三条：`X` 个数等于 `O` 或比 `O` 多 1；`X` 赢则必须多 1；`O` 赢则必须一样多。

```python
def valid_tic_tac_toe(board):
    x = sum(row.count("X") for row in board)
    o = sum(row.count("O") for row in board)
    if not (o <= x <= o + 1):   # X 先手
        return False

    lines = [list(row) for row in board]            # 行
    lines += [list(col) for col in zip(*board)]     # 列
    lines += [[board[i][i] for i in range(3)],      # 对角线
              [board[i][2 - i] for i in range(3)]]

    def wins(p):
        return any(line == [p, p, p] for line in lines)

    if wins("X") and x != o + 1:    # X 赢后 O 还在落子
        return False
    if wins("O") and x != o:        # O 赢后 X 还在落子
        return False
    return True     # 两方同时赢时两个条件互斥，必被拦下
```

**复杂度。** 时间 `O(1)`，空间 `O(1)`。

**易错点。**
- 只检查数量：`["XXX","OOO","   "]` 数量相等得 `True`，两方不可能同时赢。
- `X` 赢只要求 `x >= o`：`["XXX","OO ","O  "]` 得 `True`，应为 `False`（`X` 赢后 `O` 还在落子）。
- `O` 赢也只要求数量合法：`["OOO","XX ","XX "]` 得 `True`，应为 `False`。

**追问。**
- 判断某一步后的胜负（LC 1275）？：落子后只检查该步所在的行、列、对角线。
- 给出一种具体落子顺序？：取赢家获胜线的公共格子作最后一子，其余交替回放。

**同模式。** LC 1275 找出井字棋的获胜者、LC 348 设计井字棋、LC 36 有效的数独、LC 289 生命游戏
