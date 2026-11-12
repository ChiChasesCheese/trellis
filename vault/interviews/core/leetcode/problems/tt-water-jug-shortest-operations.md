---
slug: tt-water-jug-shortest-operations
---
## Q
**量水问题：最短操作序列**｜Medium

容量 `x`、`y` 的两个水壶，水源无限，操作有灌满、倒空、一壶倒入另一壶（直到倒空或对方满）。得到恰好 `z` 升（默认指两壶之和，也可指某一壶），输出操作次数最少的序列，做不到返回 `None`，`z = 0` 返回 `[]`。例：`(3, 5, 4)` 两壶之和 → 7 步，`(2, 6, 5)` → `None`。

## A
**一句话。** 先用 `gcd` 排除不可能，再把 `(a, b)` 当图的顶点、六种操作当边，从 `(0, 0)` 做 BFS，入队时记前驱，命中后回溯。

```python
def jug_steps(x, y, z, single=False):
    top = max(x, y) if single else x + y
    if z < 0 or z > top or z % gcd(x, y):   # 数论先判不可能
        return None

    def hit(a, b):
        return z in (a, b) if single else a + b == z

    start = (0, 0)
    parent = {start: None}      # 状态 -> (前驱, 操作)
    queue = deque([start])
    while queue:
        a, b = state = queue.popleft()
        if hit(a, b):
            ops = []
            while parent[state] is not None:   # 回溯到起点
                state, op = parent[state]
                ops.append(op)
            return ops[::-1]
        p_ab, p_ba = min(a, y - b), min(b, x - a)
        moves = (
            ((x, b), "fill X"), ((a, y), "fill Y"),
            ((0, b), "empty X"), ((a, 0), "empty Y"),
            ((a - p_ab, b + p_ab), "pour X->Y"),
            ((a + p_ba, b - p_ba), "pour Y->X"),
        )
        for nxt, op in moves:
            if nxt not in parent:   # 入队即标记
                parent[nxt] = ((a, b), op)
                queue.append(nxt)
    return None
```

**复杂度。** 时间 `O(x + y)`，空间 `O(x + y)`。

**易错点。**
- 倒水量不取 `min(a, y - b)`：直接倒光会让 `b` 超过容量，BFS 找到做不到的“更短”序列。
- `z` 的含义不同答案不同：`(3, 5, 4)` 两壶之和 7 步，某一壶 6 步，先问清。
- `None` 与 `[]` 混用：`z = 0` 返回 `[]`，调用方写 `if not result` 会把两者混为一谈。

**追问。**
- 只判断能不能（LC 365）？：`z <= x + y and z % gcd(x, y) == 0`，不需要 BFS。
- 再加一个壶？：状态变三元组，BFS 同理，状态数升到 `O(xyz)` 量级。

**同模式。** LC 365 水壶问题、LC 773 滑动谜题、LC 752 打开转盘锁、LC 127 单词接龙
