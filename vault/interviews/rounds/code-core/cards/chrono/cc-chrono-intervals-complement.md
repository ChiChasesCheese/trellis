---
id: cc-chrono-intervals-complement
node: chrono.intervals
type: qa
---
## Q
Busy intervals arrive from many sources; within a day `[0, 1440)` print the free windows of at least L minutes. Three steps, two traps.

## A
**Clip → merge → complement.**

1. Clip every busy interval to the day and drop the empties.
2. Merge the union ([[cc-chrono-intervals-merge-sweep]]) — *touching* busy intervals must merge, or step 3 emits a zero-length free window between them.
3. Walk the merged list emitting `[prev_end, next_start)`, plus the head `[day_start, first_start)` and the tail `[last_end, day_end)`.

Traps:
- A free stretch crossing the day boundary becomes two windows if windows may not cross it, and **each is judged against L on its own**.
- The length test is `>= L`: a 30-minute window qualifies for L = 30. Clipping to "now" can push a qualifying window below L, so filter *after* clipping, never before.
- A fully free day is one window covering the whole day; a fully busy day prints nothing. Both are separate outputs, not errors.

## Q zh
忙碌区间来自多个来源；在一天 `[0, 1440)` 内打印长度至少为 L 的空闲窗口。三个步骤，两个陷阱。

## A zh
**裁剪 → 合并 → 取补。**

1. 把每个忙碌区间裁剪到当天，丢掉空的。
2. 合并并集（[[cc-chrono-intervals-merge-sweep]]）—— *相接*的忙碌区间必须合并，否则第 3 步会在它们之间吐出一个零长度的空闲窗口。
3. 遍历合并结果，输出 `[prev_end, next_start)`，再加上头部 `[day_start, first_start)` 和尾部 `[last_end, day_end)`。

陷阱：
- 若窗口不允许跨日界，跨越日界的空闲段会变成两个窗口，而且**每个都各自与 L 比较**。
- 长度判据是 `>= L`：30 分钟的窗口满足 L = 30。裁剪到「现在」可能让原本合格的窗口掉到 L 以下，所以要在裁剪*之后*过滤，绝不能之前。
- 全天空闲就是覆盖整天的一个窗口；全天忙碌则什么都不打印。两者都是各自的输出，而不是错误。
