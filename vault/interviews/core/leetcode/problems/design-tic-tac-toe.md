---
slug: design-tic-tac-toe
---
## Q
**LC 348 设计井字棋**｜Medium

`n x n` 棋盘，`move(row, col, player)` 落子并返回获胜玩家编号（同行、同列或同对角线全是自己的棋子），无人获胜返回 `0`。要求每次 `move` 优于 `O(n^2)`。

## A
**一句话。** 不存棋盘，给每行、每列和两条对角线存带符号计数（玩家 1 加 `1`，玩家 2 减 `1`），绝对值到 `n` 即获胜。

```python
class TicTacToe:
    def __init__(self, n):
        self.n = n
        self.rows = [0] * n
        self.cols = [0] * n
        self.diag = self.anti = 0

    def move(self, row, col, player):
        d = 1 if player == 1 else -1
        self.rows[row] += d
        self.cols[col] += d
        if row == col:
            self.diag += d
        if row + col == self.n - 1:
            self.anti += d
        lines = (self.rows[row], self.cols[col],
                 self.diag, self.anti)
        return player if self.n in map(abs, lines) else 0
```

**复杂度。** `move` 为 `O(1)`，空间 `O(n)`。

**易错点。**
- 两个玩家都加 `1`：混合的一行也会数到 `n`，要用相反符号。
- 副对角线条件写成 `row == n - col`：应为 `row + col == n - 1`。
- 中心格写成 `elif`：奇数 `n` 的中心格同时在两条对角线上，两个计数都要加。

**追问。**
- 连成 `k` 个就赢（五子棋）？：计数法失效，在落子点沿四个方向数连续同色格，`O(k)`。
- 怎么判平局？：另记总步数，`n * n` 步后仍无赢家。

**同模式。** LC 794 有效的井字游戏、LC 1275 找出井字棋的获胜者、LC 622 设计循环队列、LC 303 区域和检索
