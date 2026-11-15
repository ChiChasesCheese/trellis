---
slug: my-calendar-ii
---
## Q
**LC 731 我的日程安排表 II**｜Medium

`book(start, end)` 添加区间 `[start, end)`，只要不会造成三重预订（某时刻被三个区间同时覆盖）就接受并返回 `True`，否则返回 `False` 且不添加。

## A
**一句话。** 维护两个列表：所有已订区间 `events` 和「已被两次覆盖」的区间 `overlaps`；新区间若与 `overlaps` 相交就是三重预订，否则把它和 `events` 的交集记入 `overlaps`。

```python
class MyCalendarTwo:
    def __init__(self):
        self.events = []
        self.overlaps = []       # 已被覆盖两次的区间

    def book(self, start, end):
        for s, e in self.overlaps:
            if start < e and s < end:
                return False     # 再加一层就是三层
        for s, e in self.events:
            if start < e and s < end:
                self.overlaps.append((max(s, start),
                                      min(e, end)))
        self.events.append((start, end))
        return True
```

**复杂度。** 每次 `book` 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 区间相交写成 `start <= e`：区间是左闭右开，端点相接不算重叠。
- 先加入 `events` 再检查：失败时已经污染了数据。
- 把整个新区间记入 `overlaps`：只能记与旧区间的交集。

**追问。**
- 怎样做到更快？：差分计数加线段树（动态开点），区间加 1 并查询最大值，每次 `O(log C)`。
- 允许 `k` 重预订呢？：这正是 LC 732 求最大重数的思路，改为维护最大重叠数并拒绝超过 `k`。

**同模式。** LC 729 我的日程安排表 I、LC 732 我的日程安排表 III、LC 715 Range 模块
