---
id: hi-pt-scheduler-system-design-9-retry-starvation
node: qb.lld.scheduler-system-design.points
type: qa
step: 9
---
## Q
**任务调度器（定时、周期、带优先级） · 重试与优先级饥饿**｜出自：任务调度器（定时、周期、带优先级） › 深入 3

任务失败怎么重试？高优先级任务源源不断时低优先级怎么办？

## A
**重试。** 在 `_run` 外包一层 `RetryPolicy`：失败后指数退避加随机抖动重新入定时堆，设最大次数，超过进死信记录。要求任务幂等，因为执行了一半失败和没执行在调度器看来无法区分。
**饥饿。** 老化（aging）：就绪队列里等待越久有效优先级越高；或为每个优先级保留最低份额的工作线程。
