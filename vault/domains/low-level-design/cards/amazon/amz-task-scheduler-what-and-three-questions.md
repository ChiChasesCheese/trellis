---
id: amz-task-scheduler-what-and-three-questions
node: amazon.amz-task-scheduler
type: qa
step: 1
tags: [grown]
---
## Q
任务调度器（Task Scheduler）要你设计什么？开场先问哪三个澄清问题？

## A
调度器接收「在某个时刻执行这个函数」的请求，到点就执行。三问：(1) 只有一次性的延迟任务，还是也有周期任务——决定任务执行完要不要重新入队；(2) 任务在哪个线程执行、是否允许并行——决定要不要线程池；(3) 要不要取消、任务抛异常怎么处理——决定任务要有 id 和状态。
