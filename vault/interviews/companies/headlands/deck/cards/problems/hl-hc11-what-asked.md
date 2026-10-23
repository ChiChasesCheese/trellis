---
id: hl-hc11-what-asked
node: problems.hc11-order-interval-overlap
type: qa
step: 1
---
## Q
订单区间最大重叠（Order Interval Overlap）题要做什么？四个 Part 各加什么要求？

## A
每张订单有生命周期，建模成**左闭右开**区间 `[start, end)`：start 那一刻已活，end 那一刻已不活。时间是非负整数 `long`，可接近 `Long.MAX_VALUE`（纳秒时间戳），所以实现里**只能比较，不能做 `end - start` 或 `(a+b)/2`**。

- **Part 1**：`maxOverlap(long[][] intervals)` 返回同时活着的最大订单数；`peak` 返回 `Peak(count, time)`，`time` 是**最早**达到最大值的时刻；`maxOverlapInclusive` 是闭区间版。例：`[[1,5],[2,6],[4,8]]` → 3，最早 t=4；`[[1,3],[3,5]]` → 1（闭区间版 2）；`[[0,10],[2,3],[2,3],[5,7]]` → 3，t=2；空输入 → `Peak(0,0)`。
- **Part 2**：`analyze(List<OrderEvent>)` → `Report(buy, sell, all)`；`Place(id, side, start, end)`，`Cancel(id, time)` 把区间截成 `[start, min(end, time))`。
- **Part 3**：`OnlineOverlap`，订单和撤单实时到达，随时回答「到现在为止最大重叠」和「t 时刻有几张」。
- **Part 4**：`IntervalIndex`，坐标高达 10¹⁸、更新顺序任意：坐标压缩 + 懒标记线段树，支持 `add/remove/liveAt/maxIn/max`。

输入规则：`start == end` 的空区间忽略；输入可乱序、有重复；`start < 0`、`end < start`、行长度不是 2 → `IllegalArgumentException`；`null` → `NullPointerException`；输入数组不得被修改；O(n log n)；百万区间 < 2 s。

相关原型：LeetCode 253（Meeting Rooms II，最少会议室 = 最大重叠）、731 / 732（My Calendar II / III）。考点：Part 1 考 **tie 规则**；Part 2 考把撤单翻译成改区间、按方向拆开；Part 3 的陷阱是同一时间戳内的事件顺序；Part 4 考线段树从零推出与何时该用。
