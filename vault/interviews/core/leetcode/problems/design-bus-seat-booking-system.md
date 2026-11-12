---
slug: design-bus-seat-booking-system
---
## Q
**LC 4080 设计公交车座位预订系统**｜Medium

每排座位 `A B C D`，`A` 邻 `B`、`D` 邻 `C`。订中间座位 1 秒；订靠窗座位时，相邻中间座位已订则 3 秒，否则 1 秒，耗时在预订那一刻定下。实现 `toggle(seat)`（订或退）、`getTotalTime()`（按 `toggle` 顺序的总耗时）、`getMinTime()`（任意顺序的最小总耗时）。

## A
**一句话。** 字典记每个座位预订时的耗时并维护总和，退座减去存下的耗时；最小耗时就是已订座位数（靠窗的先订）。

```python
class BusBooking:
    def __init__(self, n):
        self.cost = {}         # 座位 -> 预订时定下的耗时
        self.total = 0

    def toggle(self, seat):
        if seat in self.cost:  # 退座：减去当初存下的耗时
            self.total -= self.cost.pop(seat)
            return
        col, row = seat[0], seat[1:]
        c = 1
        if col in "AD":        # 相邻中间座位已订：3 秒
            mid = ("B" if col == "A" else "C") + row
            c = 3 if mid in self.cost else 1
        self.cost[seat] = c
        self.total += c

    def getTotalTime(self):
        return self.total

    def getMinTime(self):
        return len(self.cost)  # 靠窗先订，每个都 1 秒
```

**复杂度。** 每个操作 `O(1)`，空间 `O(已订座位数)`。

**易错点。**
- 退座后按当前座位重算总耗时：`B3`、`A3`、退 `B3`，重算得 `1`，应为 `3`（`A3` 当初已付 `3` 秒）。
- 相邻关系记错（`A` 邻 `C`）：`C3`、`A3` 误得 `4`，应为 `2`。

**追问。**
- 为什么最小耗时就是座位数？：把靠窗座位全排在中间座位之前订，没有座位会遇到已订的邻座。
- 为什么不能重算总耗时？：耗时是预订瞬间的快照，退座只影响之后的预订。

**同模式。** LC 380 O(1) 时间插入、删除和获取随机元素、LC 2349 设计数字容器系统、LC 1146 快照数组
