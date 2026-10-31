---
id: tlc-candy-crush-0-whole
node: c.candy-crush
type: qa
---
## Q
**LC 723 糖果消除**｜Medium · LC TikTok 全时段热度 26/100

给定 `m x n` 的二维整数数组 `board` 代表糖果所在的方格，不同的正整数代表不同种类的糖果，`board[i][j] == 0` 表示该位置为空。给定的是玩家移动后的状态，按规则粉碎糖果，直到状态稳定并输出：如果有三个及以上水平或垂直相连的同种糖果，**同时**将它们粉碎（变成空）；粉碎后，空位上方的糖果同时下落直到碰到下方糖果或底部，顶部不会有新糖果出现；重复以上两步直到没有可粉碎的糖果。`m == board.length`，`n == board[i].length`，`3 <= m, n <= 50`，`1 <= board[i][j] <= 2000`。例：`board = [[1,3,5,5,2],[3,4,3,3,1],[3,2,4,5,2],[2,4,4,5,5],[1,4,4,1,1]]` → `[[1,3,0,0,0],[3,4,0,5,2],[3,2,0,3,1],[2,4,0,5,2],[1,4,3,1,1]]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 直接模拟：每轮先扫一遍把所有横向、纵向的三连（及以上）格子**都标记**出来，没有就结束；有就一起清零，再逐列让非零糖果下落，循环直到稳定。

**识别。** 规则本身就是算法，难点在两个「同时」：同一轮里标记完再统一清除，下落也按列整体处理。`3 <= m, n <= 50` 允许每轮 `O(mn)`、轮数最多 `O(mn)`。

**推导。** 一个糖果可能同时属于横向和纵向的三连（L 型、T 型），所以不能边找边清零，否则会破坏另一方向的三连判断。做法：第一遍只收集要粉碎的坐标，第二遍统一清零。下落按列：把该列非零糖果按原顺序取出，放到列底，上面补零。每轮至少粉碎 3 个糖果，所以最多 `mn / 3` 轮。

```python
def candy_crush(board: list[list[int]]) -> list[list[int]]:
    m, n = len(board), len(board[0])
    while True:
        crush: set[tuple[int, int]] = set()      # 本轮要粉碎的坐标，标记完才统一清除
        for r in range(m):
            for c in range(n):
                v = board[r][c]
                if v == 0:
                    continue
                if c + 2 < n and board[r][c + 1] == v == board[r][c + 2]:
                    crush |= {(r, c), (r, c + 1), (r, c + 2)}     # 横向三连（更长的连续由相邻起点补全）
                if r + 2 < m and board[r + 1][c] == v == board[r + 2][c]:
                    crush |= {(r, c), (r + 1, c), (r + 2, c)}     # 纵向三连
        if not crush:
            return board                         # 稳定了
        for r, c in crush:
            board[r][c] = 0
        for c in range(n):                       # 逐列下落：非零糖果保持顺序沉到底部
            column = [board[r][c] for r in range(m) if board[r][c]]
            column = [0] * (m - len(column)) + column
            for r in range(m):
                board[r][c] = column[r]
```

运行：示例 2 → `[[1,3,0,0,0],[3,4,0,5,2],[3,2,0,3,1],[2,4,0,5,2],[1,4,3,1,1]]`；`[[1,1,1],[2,3,4],[5,6,7]]` → `[[0,0,0],[2,3,4],[5,6,7]]`；`[[1,2,3],[4,5,6],[7,8,9]]` → 原样；`[[1,1,1],[0,1,0],[0,1,0]]`（T 型）→ 全 `0`。

**复杂度。** 时间 `O((mn)²)` 最坏（`mn / 3` 轮，每轮 `O(mn)`）；空间 `O(mn)`（标记集合）。

**拓展优化。**
- 额外空间 `O(1)`：不用集合，把要粉碎的格子在原矩阵里取负数做标记，`abs` 还原判断值；下落时用写指针从底往上压实。

```python
def candy_crush_in_place(board: list[list[int]]) -> list[list[int]]:
    m, n = len(board), len(board[0])
    while True:
        found = False
        for r in range(m):
            for c in range(n - 2):
                v = abs(board[r][c])             # 负数是本轮已标记，仍代表同一种糖果
                if v and v == abs(board[r][c + 1]) == abs(board[r][c + 2]):
                    found = True
                    board[r][c] = board[r][c + 1] = board[r][c + 2] = -v
        for c in range(n):
            for r in range(m - 2):
                v = abs(board[r][c])
                if v and v == abs(board[r + 1][c]) == abs(board[r + 2][c]):
                    found = True
                    board[r][c] = board[r + 1][c] = board[r + 2][c] = -v
        if not found:
            return board
        for c in range(n):
            write = m - 1                        # 写指针：下一个非零糖果该落的行
            for r in range(m - 1, -1, -1):
                if board[r][c] > 0:              # 负数和零都跳过（被粉碎或本来为空）
                    board[write][c] = board[r][c]
                    write -= 1
            for r in range(write, -1, -1):
                board[r][c] = 0                  # 上面剩下的位置补零
```

**易错点。**
- 边找边清零：先清横向三连会破坏纵向三连，`[[1,1,1],[0,1,0],[0,1,0]]` 只清掉一部分，得到 `[[0,0,0],[0,1,0],[0,1,0]]`，正确是全 `0`。
- 只做一轮就返回：下落后可能出现新的三连，必须循环到稳定。
- 下落时打乱顺序：糖果落下后保持原来自上而下的相对顺序。

**追问。**
- 每次粉碎要计分（比如粉碎 `k` 个得 `k²` 分）：在清零前累加。
- 顶部会补充新糖果：下落后把空位按随机或给定序列填满，再继续循环。

**同模式。** LC 529 扫雷游戏、LC 289 生命游戏、LC 54 螺旋矩阵、LC 48 旋转图像、LC 1031 两个非重叠子数组的最大和。
