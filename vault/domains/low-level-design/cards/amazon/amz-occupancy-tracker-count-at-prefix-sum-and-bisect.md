---
id: amz-occupancy-tracker-count-at-prefix-sum-and-bisect
node: amazon.amz-occupancy-tracker
type: qa
step: 4
tags: [grown]
---
## Q
在办公室人数追踪里，`count_at(t)` 怎样做到 O(log n)？给一个具体输入和输出。

## A
事件按时间追加，时间数组有序，前缀和数组 `counts[i]` 是处理完第 i 个事件后的人数。`i = bisect_right(times, t) - 1` 找到最后一个时间不晚于 t 的事件，答案是 `counts[i]`，没有则为 0。追加 O(1)，查询 O(log n)。用 `bisect_right` 是因为时间等于 t 的事件也算。例：事件 a进@10、b进@20、c进@30、a出@40、d进@40，前缀和 `[1,2,3,2,3]`：`count_at(25)` 得 2，`count_at(40)` 得 3。
