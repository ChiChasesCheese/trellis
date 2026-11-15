---
slug: seat-reservation-manager
---
## Q
**LC 1845 座位预约管理系统**｜Medium

设计座位系统，座位编号 `1` 到 `n`。`reserve()` 预订编号最小的空座位并返回编号；`unreserve(seatNumber)` 释放该座位。

## A
**一句话。** 用计数器 `nxt` 表示"从未用过的最小座位"，再用小根堆保存被释放的座位；预订时先看堆，空了才用 `nxt`。

```python
class SeatManager:
    def __init__(self, n):
        self.nxt = 1               # 从没分配过的最小座位
        self.heap = []             # 被释放的座位

    def reserve(self):
        if self.heap:
            return heappop(self.heap)
        self.nxt += 1
        return self.nxt - 1

    def unreserve(self, seat_number):
        heappush(self.heap, seat_number)
```

**复杂度。** `reserve`、`unreserve` 均 `O(log n)`，空间 `O(n)`。

**易错点。**
- 一开始把 `1..n` 全塞进堆：`O(n)` 初始化，`n` 很大时浪费。
- 先用 `nxt` 再看堆：释放的座位编号一定小于 `nxt`，必须先取堆里的。

**追问。**
- 为什么堆里的永远比 `nxt` 小？：只有已分配过的座位才能被释放，而分配过的编号都小于 `nxt`。

**同模式。** LC 146 LRU 缓存、LC 295 数据流的中位数、LC 2034 股票价格波动
