---
id: tlc-tt-water-jug-shortest-operations-2-code
node: p4.tt-water-jug-shortest-operations
type: qa
step: 2
---
## Q
**量水问题：最短操作序列**｜写出 Python 实现

写 `jug_steps(x, y, z, single=False)`：容量 `x`、`y` 升的两个水壶（`1 <= x, y <= 10^3`），水源无限，操作是灌满某个壶、倒空某个壶、把一个壶倒进另一个（直到自己空或对方满）。`single=False` 时目标是两壶水量之和为 `z`，`True` 时是某一个壶里恰好 `z` 升。返回操作次数最少的操作名列表（`"fill X"`、`"pour X->Y"` 等），做不到返回 `None`，`z = 0` 返回 `[]`。

## A
**思路。** 先排除 `z` 超过上限或不是 `gcd(x, y)` 倍数的情形。然后以 `(a, b)` 为状态从 `(0, 0)` 做 BFS：每个状态展开六种操作，新状态入队时记 `(前驱状态, 操作名)`，第一次满足目标就回溯。

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

运行：`(3, 5, 4)` → `['fill X', 'pour X->Y', 'fill X', 'pour X->Y', 'empty Y', 'pour X->Y', 'fill X']`；`(3, 5, 4, single=True)` → `['fill Y', 'pour Y->X', 'empty X', 'pour Y->X', 'fill Y', 'pour Y->X']`；`(2, 6, 5)` → `None`，`(3, 5, 0)` → `[]`，`(1, 1, 2)` → `['fill X', 'fill Y']`，`(4, 6, 6, single=True)` → `['fill Y']`，`(3, 5, 9)` → `None`；`(97, 100, 99)` → `131` 步，`(100, 99, 1)` → `3` 步。

**复杂度。** 时间与空间 `O(x + y)`：可达状态至多 `2(x + y + 2)` 个，每个展开 `6` 条边。

**写法要点。**
- `a, b = state = queue.popleft()`：链式赋值同时得到整个状态元组和它的两个分量，回溯时直接用 `state`。
- `parent` 既是已访问集合又是前驱表，值是 `(前驱状态, 操作名)`，起点映射到 `None` 作为回溯终止标志。
- 倒水量 `min(a, y - b)`、`min(b, x - a)` 先算好，六种后继写成一个元组列表，循环处理，避免六段重复代码。
- 内层函数 `hit` 封装目标判定：`single` 开关只改这一处，主流程不变。
