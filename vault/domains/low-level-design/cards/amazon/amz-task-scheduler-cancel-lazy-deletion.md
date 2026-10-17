---
id: amz-task-scheduler-cancel-lazy-deletion
node: amazon.amz-task-scheduler
type: qa
step: 5
tags: [grown]
---
## Q
在任务调度器设计里，取消一个还在堆里的任务，为什么用惰性删除而不是直接从堆里删？

## A
堆中间删一个元素是 O(n)（要先找到再重建）。惰性删除：只把 `task.cancelled = True`，调度线程弹到它时直接跳过，取消是 O(1)。代价：堆里留着垃圾，所以另外维护「待执行数」，垃圾超过一半时 `heapify` 重建一次。已经开始运行的任务取消不了，`cancel` 要返回 False 告诉调用方。
