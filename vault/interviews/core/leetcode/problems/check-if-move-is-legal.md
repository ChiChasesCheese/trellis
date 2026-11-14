---
slug: check-if-move-is-legal
---
## Q
**LC 1958 检查操作是否合法**｜Medium

`8×8` 黑白棋盘，把颜色 `color` 的棋下在空格 `(rMove, cMove)`。若某个方向上从它出发是「至少一枚连续异色棋，再接一枚同色棋」，就合法。

## A
**一句话。** 八个方向各走一遍：先跳过连续的异色棋，至少跳过一枚，且停下的格子是同色棋，就成立。

```python
def check_move(board, r_move, c_move, color):
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == dc == 0:
                continue
            r, c, n = r_move + dr, c_move + dc, 0
            while (0 <= r < 8 and 0 <= c < 8
                   and board[r][c] not in ('.', color)):
                r, c, n = r + dr, c + dc, n + 1   # 异色棋
            if (n and 0 <= r < 8 and 0 <= c < 8
                    and board[r][c] == color):
                return True
    return False
```

**复杂度。** 时间 `O(8·8)`，空间 `O(1)`。

**易错点。**
- 没要求至少一枚异色棋：紧挨着同色棋（`n = 0`）不算合法的「好线段」。
- 出界后还读 `board[r][c]`：负下标在 Python 里不报错，会读到棋盘另一边。

**追问。**
- 推广到 `n×n`？：同样八方向，每个方向最多走 `n` 步，`O(n)`。
- 还要真的落子翻转？：对每个成立的方向，把途经的异色棋改成 `color`。

**同模式。** LC 36 有效的数独、LC 1275 找出井字棋的获胜者、LC 999 可以被一步捕获的棋子数
