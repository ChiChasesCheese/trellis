---
id: amz-task-scheduler-objects-and-jobs
node: amazon.amz-task-scheduler
type: qa
step: 2
tags: [grown]
---
## Q
在任务调度器设计里应该有哪几个对象？各自只负责一件什么事？

## A
`Task`：函数、到期时间、周期（可为空）、是否已取消。`Scheduler`：持有按到期时间排序的最小堆，一把锁加一个条件变量（condition variable，让线程睡到「有新任务或到点」才醒）。`Worker` 线程池：真正执行任务。返回给调用方的是任务 id，用于取消。切分依据：「何时执行」和「在哪执行」分属两个角色。
