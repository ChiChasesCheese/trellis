---
id: hi-pt-elevator-design-3-look
node: qb.lld.elevator-design.points
type: qa
step: 3
---
## Q
**电梯系统 · LOOK 扫描**｜必会 · 出自：电梯系统 › 深入 1

单部电梯的调度策略 FCFS、SCAN、LOOK、SSTF 怎么比？为什么选 LOOK，它为什么不会饥饿？

## A
**对比。** FCFS 公平但来回折腾；SCAN 扫到楼顶/楼底再掉头，无饥饿但空跑端点；SSTF 效率高但边缘楼层会被近处请求一直挤掉（饥饿）。
**选择。** LOOK：走到该方向最远的请求就掉头，行程短；每次掉头后总会扫过所有请求，所以无饥饿。
