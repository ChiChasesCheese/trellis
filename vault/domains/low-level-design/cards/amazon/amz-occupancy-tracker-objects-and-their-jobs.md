---
id: amz-occupancy-tracker-objects-and-their-jobs
node: amazon.amz-occupancy-tracker
type: qa
step: 2
tags: [grown]
---
## Q
在办公室人数追踪设计里，应有哪几个对象？各自只负责什么？

## A
系统是「一条只追加的事件日志 + 从日志累加出来的人数」。`Event`：一次进出（时间、人、区域、+1 或 −1）的不可变记录。`Timeline`：一条只追加的时间线，拥有时间数组、前缀和数组和区间最大值线段树，回答 `count_at` 与 `max_in`。`OccupancyTracker`：校验事件合法并写进相关时间线。错误类：`AlreadyInside`、`NotInside`、`OutOfOrder`。不变量：时间数组非递减，与前缀和数组等长。
