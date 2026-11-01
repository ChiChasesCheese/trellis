---
id: tlc-valid-tic-tac-toe-state-2-code
node: p3.valid-tic-tac-toe-state
type: qa
step: 2
---
## Q
**LC 794 有效的井字游戏**｜写出 Python 实现

给定长度为 `3` 的字符串数组 `board`，每个字符串长 `3`，字符为 `'X'`、`'O'` 或 `' '`。玩家 1 先放 `'X'`，玩家 2 放 `'O'`，轮流落子，有一方连成三个（行、列或对角线）游戏立即结束。返回这个盘面是否可能在一局游戏中出现。

## A
**思路。** 数出 `X`、`O` 的个数，找出两方各自是否连线；盘面合法当且仅当 `O <= X <= O + 1`，且 `X` 连线时 `X == O + 1`，`O` 连线时 `X == O`。

```python
def valid_tic_tac_toe(board: list[str]) -> bool:
    x = sum(row.count("X") for row in board)
    o = sum(row.count("O") for row in board)
    if not (o <= x <= o + 1):
        return False                             # X 先手：任何时刻 X 比 O 多 0 或 1 子

    lines = [list(row) for row in board]                              # 3 行
    lines += [list(col) for col in zip(*board)]                       # 3 列
    lines += [[board[i][i] for i in range(3)], [board[i][2 - i] for i in range(3)]]   # 2 条对角线

    def wins(p: str) -> bool:
        return any(line == [p, p, p] for line in lines)

    if wins("X") and x != o + 1:
        return False                             # X 赢 = X 刚落完最后一子；若 x == o，说明 X 赢后 O 还在落子
    if wins("O") and x != o:
        return False                             # O 赢 = O 刚落完最后一子；若 x == o + 1，说明 O 赢后 X 还在落子
    return True                                  # X、O 同时赢时 x == o + 1 与 x == o 互斥，必被上面拦下
```

运行：`["O  ","   ","   "]` → `False`，`["XOX"," X ","   "]` → `False`，`["XOX","O O","XOX"]` → `True`；`["XXX","OO ","   "]` → `True`，`["XXX","OOO","   "]` → `False`，`["XXX","OO ","O  "]` → `False`，`["OOO","XX ","XX "]` → `False`，`["   ","   ","   "]` → `True`。

**复杂度。** 时间 `O(1)`（棋盘固定 `3 x 3`），空间 `O(1)`。

**写法要点。**
- `zip(*board)` 把三个字符串转置成三列，行和列用同一种「长度为 3 的列表」表示，`wins` 只写一次。
- `row.count("X")` 对每行直接计数，不用手写双层循环。
- `any(line == [p, p, p] for line in lines)` 一行表达「任意一条线全是 `p`」；对角线用下标推导式，副对角线是 `board[i][2 - i]`。
- 先过滤数量，再判断连线：数量不对时不需要构造 `lines`。
