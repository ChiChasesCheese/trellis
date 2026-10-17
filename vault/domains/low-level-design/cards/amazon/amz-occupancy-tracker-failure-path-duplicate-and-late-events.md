---
id: amz-occupancy-tracker-failure-path-duplicate-and-late-events
node: amazon.amz-occupancy-tracker
type: qa
step: 7
tags: [grown]
---
## Q
在办公室人数追踪里，刷卡事件被重发、或者比已入账的事件更晚到达，该怎么处理？

## A
重发：与该人最近一次事件完全相同（时间、区域、方向都一样）才算重试，忽略并返回 `False`；内容不同才是非法序列，抛 `AlreadyInside` 或 `NotInside`。只为每人保存最近一条，内存随人数增长。迟到：时间比最后一个已入账事件更早，抛 `OutOfOrder`，因为插入中间会让后面所有前缀和失效。要接受乱序，用水位线缓冲（等 T−5 分钟之前的到齐再入账），或换 Fenwick 树。拒绝时不改变任何状态。
