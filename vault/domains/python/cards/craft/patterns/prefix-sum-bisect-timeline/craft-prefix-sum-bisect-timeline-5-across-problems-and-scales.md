---
id: craft-prefix-sum-bisect-timeline-5-across-problems-and-scales
node: craft.patterns.prefix-sum-bisect-timeline
type: qa
step: 5
---
## Q
**前缀和时间线 · 会议室、人数追踪、票价、账本历史余额里的同一个扫描**｜模式

Meeting Rooms II、办公室人数追踪、地铁票价、账本的历史余额，看起来分别是区间、进出记录、线路和账目。它们共享什么？放大到时序数据库，这是什么？

## A
**要点。** 都是：把"状态"拆成"状态的变化量（事件）"，状态等于变化量的前缀和；按顺序排好以后，任一点的状态是一次二分，任一段的极值是"基线 + 段内变化"。

```python
# Meeting Rooms II（LeetCode 253）：把区间变成 +1/-1 事件，前缀和的最大值就是答案
events = sorted([(s, 1) for s, _ in intervals] + [(e, -1) for _, e in intervals])
cur = best = 0
for _, d in events: cur += d; best = max(best, cur)
# amz-occupancy-tracker：同一份事件，按时间二分
i = bisect.bisect_right(self._times, ts) - 1
# double-entry-ledger.balance_at：键是分录序号
i = bisect_right(hist, seq, key=lambda line: line.seq)
```

**见于。** meeting-rooms-ii、amz-occupancy-tracker、amz-train-fare、double-entry-ledger。

**不变的。** 存变化量不存总量；前缀和数组与键（时间或序号）并排；查询是 `bisect_right` 减一；起点要补基线。**变化的。** 键是什么（时间、序号、位置）；要的是某点的值，还是一段上的最大值。

**细节。** 同一时刻既有结束又有开始时：`(t, -1)` 排在 `(t, 1)` 前面，所以先减后加，端点相接的会议不占两个房间。排序键里的这个"平局规则"就是业务语义（一个会议结束的瞬间可以立刻开始下一个）。

**信号。** 需求里出现"同时在线""峰值""高峰时段""某一刻的余额""历史任意时刻的状态"；输入是区间或进出事件。

**尺度对照。** 力扣：扫描线求最大重叠数。低层设计：追加型时间线 + 二分 + 区间最大。分布式：时序数据库与流处理里的窗口聚合（滑动窗口内的计数、峰值，每个事件到来时更新窗口状态）；账单里按事件时间归档的用量。变化：事件不再按时间有序到达，要么用水位线（watermark）等迟到的数据再关闭窗口，要么允许对历史前缀和做修正（这时单机里"只能追加"的前提被打破，要用能修改的结构，如树状数组）。
