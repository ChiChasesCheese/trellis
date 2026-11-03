---
id: craft-dispatch-tables-2-direction-table
node: craft.idioms.dispatch-tables
type: qa
step: 2
---
## Q
**分派表 · 四子连珠为什么只列四个方向**｜写法

四子连珠（Connect Four）落子后要检查横、竖、两条斜线是否连成四个。常见写法是四段几乎一样的循环，或者八个方向各写一遍。方向表怎样让它变成一段代码，为什么只需要列四个方向，而不是八个？

## A
**要点。** 一条直线有两个方向，沿线数相同的棋子时，正方向和反方向是同一条线上的两边。所以只列四个方向 `(0,1) (1,0) (1,1) (1,-1)`（横、竖、斜、反斜），每个方向在同一个函数里往两边各数一次，再加上自己。把方向放进数据，要改规则（例如五子连珠）只改常量，不改逻辑。

```python
ROWS, COLS, CONNECT = 6, 7, 4
_DIRECTIONS = ((0, 1), (1, 0), (1, 1), (1, -1))      # 横、竖、斜、反斜；另一半是反方向

def count_line(grid, r, c, dr, dc) -> int:
    """从 (r, c) 出发，沿 (dr, dc) 和它的反方向各数一边，加上自己。"""
    me, total = grid[r][c], 1
    for sign in (1, -1):                              # 同一段代码走两个方向
        rr, cc = r + sign * dr, c + sign * dc
        while 0 <= rr < ROWS and 0 <= cc < COLS and grid[rr][cc] == me:
            total += 1
            rr, cc = rr + sign * dr, cc + sign * dc
    return total

def wins(grid, r, c) -> bool:
    return any(count_line(grid, r, c, dr, dc) >= CONNECT for dr, dc in _DIRECTIONS)

grid = [["."] * COLS for _ in range(ROWS)]
for i in range(4):                                    # 反斜线：(5,0) (4,1) (3,2) (2,3)
    grid[5 - i][i] = "X"
print(wins(grid, 3, 2))
grid[3][2] = "."
print(wins(grid, 4, 1))
```

实际输出：

```
True
False
```

**为什么。** 只检查最后落下的那一格，因为之前没有连成四个，新的连线必然经过它。在一条线上从中间往两边数，比枚举每个起点更省，也不会重复计数。

**信号。** 网格上「沿几个方向扫描」的问题（岛屿、单词搜索、棋类）都适合方向表。要注意一个反例：四邻域的上下左右，用的是四个方向各走一步，并不是「一条线的两端」，这时方向表要列全。
