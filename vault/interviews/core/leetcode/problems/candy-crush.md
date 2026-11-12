---
slug: candy-crush
---
## Q
**LC 723 糖果消除**｜Medium

`board` 中正整数是糖果种类，`0` 是空位。同时粉碎所有横向或纵向三连及以上的同种糖果，上方糖果下落，重复到稳定，返回最终棋盘。

## A
**一句话。** 模拟：每轮先标记全部三连、再统一清零、逐列下落，直到没有可粉碎的。

```python
def candy_crush(board):
    m, n = len(board), len(board[0])
    while True:
        crush = set()        # 标记完才统一清除
        for r in range(m):
            for c in range(n):
                v = board[r][c]
                if v == 0:
                    continue
                if c + 2 < n and \
                        board[r][c+1] == v == board[r][c+2]:
                    crush |= {(r, c), (r, c+1), (r, c+2)}
                if r + 2 < m and \
                        board[r+1][c] == v == board[r+2][c]:
                    crush |= {(r, c), (r+1, c), (r+2, c)}
        if not crush:
            return board
        for r, c in crush:
            board[r][c] = 0
        for c in range(n):   # 逐列下落，保持相对顺序
            col = [board[r][c] for r in range(m)
                   if board[r][c]]
            col = [0] * (m - len(col)) + col
            for r in range(m):
                board[r][c] = col[r]
```

**复杂度。** 时间 `O((mn)^2)`，空间 `O(mn)`。

**易错点。**
- 边找边清零：先清横向会破坏纵向三连，`[[1,1,1],[0,1,0],[0,1,0]]` 只清掉一部分。
- 只做一轮：下落后可能出现新的三连，必须循环到稳定。

**追问。**
- 每次粉碎要计分？：清零前累加粉碎的格数。
- 原地标记不用 set？：用负数标记待粉碎，判断时取绝对值。

**同模式。** LC 289 生命游戏、LC 529 扫雷游戏、LC 48 旋转图像、LC 54 螺旋矩阵
