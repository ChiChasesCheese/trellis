---
id: hi-c-sd-long-running-tasks-n13-backpressure
node: sd.patterns.long-running-tasks.notes
type: qa
step: 14
---
## Q
**长任务 · 追问：流量暴涨十倍，队列堆成山**｜摘要 · 追问

黑色星期五任务量是平时十倍，队列积压数百万，怎么办？

## A
- **后果：** 队列无限增长，内存暴涨，任务等待数小时，新任务因队列满被拒绝，用户一直等不到结果。
- **背压（backpressure）：** 工作者忙不过来时减慢任务接受。设置队列深度上限，队列太深就拒绝新任务并立刻返回"系统繁忙"，而不是接下处理不了的工作。
- **按队列深度自动扩容工作者：** 超过阈值就多开，缩短就减少。AWS 上 CloudWatch 告警配合 Auto Scaling 组可以实现。
- **关键指标是队列深度，不是 CPU：** CPU 高的时候队列已经堵了。
