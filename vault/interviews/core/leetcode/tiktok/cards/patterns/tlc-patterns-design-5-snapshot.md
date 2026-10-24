---
id: tlc-patterns-design-5-snapshot
node: patterns.design
type: qa
step: 5
---
## Q
**数据结构设计题｜快照数组（LC 1146）：只记录变化，查询时二分**

每次 `snap()` 都复制整个数组为什么不行？怎样存储才能让 `set`、`snap` 都是 `O(1)`、`get` 是 `O(log n)`？

## A
长度 `50000`、操作最多 `50000` 次：每次 `snap` 复制整个数组是 `50000 × 50000`，太大。改成**只记录发生过变化的下标**：每个下标存一个升序的 `(快照号, 值)` 列表。

```python
from bisect import bisect_right
class SnapshotArray:
    def __init__(self, length: int) -> None:
        self.snap_id = 0
        self.history: list[list[tuple[int, int]]] = [[(0, 0)] for _ in range(length)]

    def set(self, index: int, val: int) -> None:
        h = self.history[index]
        if h[-1][0] == self.snap_id:
            h[-1] = (self.snap_id, val)    # 同一个快照期内多次 set：覆盖
        else:
            h.append((self.snap_id, val))

    def snap(self) -> int:
        self.snap_id += 1
        return self.snap_id - 1

    def get(self, index: int, snap_id: int) -> int:
        h = self.history[index]
        i = bisect_right(h, (snap_id, float("inf"))) - 1   # 最后一个 快照号 <= snap_id 的记录
        return h[i][1]

sa = SnapshotArray(3)
sa.set(0, 5)
print(sa.snap())      # 0
sa.set(0, 6)
print(sa.get(0, 0))   # 5
```

- `snap()` 只是把计数器加一，`O(1)`；`set` 是 `O(1)`；`get` 在该下标的历史里二分，`O(log k)`。总空间与 `set` 次数成正比。
- `bisect_right(h, (snap_id, inf))` 把元组与 `(snap_id, inf)` 比较，找出快照号 `<= snap_id` 的最后一条记录；初始记录 `(0, 0)` 保证一定存在。
- 题目中 `snap_id` 是"调用 `snap()` 的次数减 1"：第一次快照返回 `0`。`set` 发生在快照号 `snap_id` 的区间内，`get(.., s)` 要的是第 `s` 次快照**之前**的最后一次写入。
- 同类思路：带时间戳的键值存储（按时间戳二分）、版本化文档。
