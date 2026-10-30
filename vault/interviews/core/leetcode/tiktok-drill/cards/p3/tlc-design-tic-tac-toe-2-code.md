---
id: tlc-design-tic-tac-toe-2-code
node: p3.design-tic-tac-toe
type: qa
step: 2
---
## Q
**LC 348 设计井字棋**｜写出 Python 实现

写类 `TicTacToe(n)`：`move(row, col, player)` 在 `(row, col)` 落下玩家 `player`（`1` 或 `2`）的棋子，返回落子后获胜的玩家编号，没有人获胜返回 `0`。`2 <= n <= 100`，`0 <= row, col < n`，每次落子的位置互不相同，最多 `n^2` 次调用。要求每次 `move` 比 `O(n^2)` 更快。

## A
**思路。** 用带符号的计数代替棋盘：每行、每列、主对角线、副对角线各一个计数，玩家 1 加 `1`，玩家 2 减 `1`；落子后检查它影响的计数，绝对值等于 `n` 就是整条线同色。

```python
class TicTacToe:
    def __init__(self, n: int) -> None:
        self.n = n
        self.rows = [0] * n
        self.cols = [0] * n
        self.diag = self.anti = 0

    def move(self, row: int, col: int, player: int) -> int:
        d = 1 if player == 1 else -1            # 玩家 1 记 +1，玩家 2 记 -1
        self.rows[row] += d
        self.cols[col] += d
        if row == col:
            self.diag += d
        if row + col == self.n - 1:
            self.anti += d
        if self.n in (abs(self.rows[row]), abs(self.cols[col]), abs(self.diag), abs(self.anti)):
            return player
        return 0
```

运行：`n = 3`，`move(0,0,1)`、`move(0,2,2)`、`move(2,2,1)`、`move(1,1,2)`、`move(2,0,1)`、`move(1,0,2)`、`move(2,1,1)` → `[0, 0, 0, 0, 0, 0, 1]`；玩家 2 占满副对角线 `(0,2)`、`(1,1)`、`(2,0)` 时最后一步返回 `2`；`n = 2` 下 `(0,0,1)`、`(0,1,2)`、`(1,0,1)` → `0, 0, 1`。

**复杂度。** `move` 为 `O(1)`，空间 `O(n)`。

**写法要点。**
- 一个带符号的数同时编码「几个子」和「是谁的」，比每个玩家各存一份计数更省，判断也只需要 `abs`。
- `self.n in (abs(...), abs(...), abs(...), abs(...))` 用成员测试代替四个 `or`，一行表达「任意一条线满了」。
- `self.diag = self.anti = 0` 链式赋值初始化两个同值的标量；列表则必须分开写 `[0] * n`，`rows = cols = [0] * n` 会让两者共用同一个列表。
- 副对角线条件是 `row + col == n - 1`；中心格两个条件都成立，所以用两个独立的 `if`，不要写 `elif`。
