---
id: tlc-tt-water-jug-shortest-operations-0-whole
node: p5.tt-water-jug-shortest-operations
type: qa
---
## Q
**量水问题：最短操作序列**｜Medium · 近一年被问：美国 2 次、国内 0 次 · 最近 2026-05-08（面试记录）

两个容量分别为 `x`、`y` 升的水壶，水源无限。允许三种操作：把任一水壶灌满；把任一水壶倒空；把一个水壶的水倒进另一个，直到倒的壶空了或者另一个壶满了。要得到恰好 `z` 升水（先和面试官确认 `z` 的含义：默认是两个壶里的水量之和，也可以是「某一个壶里」），**输出操作次数最少的操作序列**，做不到返回 `None`，`z = 0` 返回空列表。`1 <= x, y <= 10^3`，`0 <= z <= 2 * 10^3`。例：`x = 3`，`y = 5`，`z = 4`：两壶之和 → `['fill X', 'pour X->Y', 'fill X', 'pour X->Y', 'empty Y', 'pour X->Y', 'fill X']`（`7` 步）；某一个壶里 → `['fill Y', 'pour Y->X', 'empty X', 'pour Y->X', 'fill Y', 'pour Y->X']`（`6` 步）；`x = 2`，`y = 6`，`z = 5` → `None`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 先用数论排除不可能的情形（`z` 超过上限，或者不是 `gcd(x, y)` 的倍数）；然后把状态 `(a, b)`（两壶当前水量）当作图的顶点，六种操作当作边，从 `(0, 0)` 做 BFS，入队时记前驱，第一次满足目标就沿前驱回溯得到最短操作序列。

**识别。** 「最少操作次数」加「状态是（壶一水量，壶二水量）」是隐式图上的最短路，无权图用 BFS；「输出序列」就是在 BFS 里多记一个前驱。能不能做到有数论判据（LC 365）：`z` 必须是 `gcd(x, y)` 的倍数，且不超过 `x + y`（单壶版不超过 `max(x, y)`）。

**推导。** 暴力：用 DFS 随便找一条操作序列，不保证最短，还可能陷入环。浪费：DFS 沿着一条路走到底，没有利用“每一步等代价”这件事。洞察：每个操作代价都是 `1`，BFS 按层展开，第一次到达目标的路径就是最短的；状态总数看似是 `(x+1)(y+1)`，其实每次操作之后总有一个壶是空的或满的，可达状态至多 `2(x + y + 2)` 个，BFS 很快。

```python
from collections import deque
from math import gcd


def jug_steps(x: int, y: int, z: int, single: bool = False) -> list[str] | None:
    """两个水壶容量 x、y。得到恰好 z 升（single=False：两壶之和；True：某一壶里）的最短操作序列；做不到返回 None。"""
    top = max(x, y) if single else x + y
    if z < 0 or z > top or z % gcd(x, y):          # 先用数论判不可能，免得白白搜遍整个状态空间
        return None

    def hit(a: int, b: int) -> bool:
        return z in (a, b) if single else a + b == z

    start = (0, 0)
    parent: dict[tuple[int, int], tuple[tuple[int, int], str] | None] = {start: None}
    queue = deque([start])
    while queue:
        a, b = state = queue.popleft()
        if hit(a, b):
            ops: list[str] = []
            while parent[state] is not None:       # 沿前驱回溯到起点
                state, op = parent[state]
                ops.append(op)
            return ops[::-1]
        pour_ab, pour_ba = min(a, y - b), min(b, x - a)
        moves = (((x, b), "fill X"), ((a, y), "fill Y"), ((0, b), "empty X"), ((a, 0), "empty Y"),
                 ((a - pour_ab, b + pour_ab), "pour X->Y"), ((a + pour_ba, b - pour_ba), "pour Y->X"))
        for nxt, op in moves:
            if nxt not in parent:
                parent[nxt] = ((a, b), op)
                queue.append(nxt)
    return None
```

运行：`(3, 5, 4)` → 七步（两壶之和）；`(3, 5, 4, single=True)` → 六步；`(2, 6, 5)` → `None`（`gcd = 2`，`5` 不是倍数）；`(3, 5, 0)` → `[]`；`(1, 1, 2)` → `['fill X', 'fill Y']`；`(4, 6, 6, single=True)` → `['fill Y']`；`(3, 5, 8)` → `['fill X', 'fill Y']`；`(3, 5, 9)` → `None`（超过 `x + y`）；`(97, 100, 99)` → 131 步，`(100, 99, 1)` → 3 步。

**复杂度。** 时间与空间 `O(x + y)`（可达状态至多 `2(x + y + 2)` 个，每个状态展开 `6` 条边）。

**易错点。**
- `z` 的含义不同答案不同：`(3, 5, 4)` 两壶之和要 `7` 步，某一个壶里只要 `6` 步。先问清楚。
- 倒水量必须取 `min(a, y - b)`：直接倒光会让 `b` 超过容量 `y`，出现不可能的状态，BFS 会找到根本做不到的“更短”序列。
- 区分 `None` 与 `[]`：`z = 0` 不需要任何操作，返回 `[]`；`None` 表示做不到。调用方写 `if not result` 会把两者混为一谈，要写 `if result is None`。
- 前驱要在入队时记录、同时当作已访问：出队时才标记会让同一个状态重复入队。

**追问。**
- 只判断能不能（LC 365）：`z <= x + y and z % gcd(x, y) == 0`，`O(log)`，不需要 BFS。
- 两个壶之外再加一个壶：状态变成三元组，BFS 同理，状态数上升到 `O(xyz)` 量级。
- 输出每一步之后两个壶的水量：回溯时把 `state` 一并记下来，或者按操作序列再模拟一遍。

**同模式。** LC 365 水壶问题、LC 773 滑动谜题、LC 752 打开转盘锁、LC 127 单词接龙。
