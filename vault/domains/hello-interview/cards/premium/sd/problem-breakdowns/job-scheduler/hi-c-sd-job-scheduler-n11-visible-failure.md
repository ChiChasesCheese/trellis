---
id: hi-c-sd-job-scheduler-n11-visible-failure
node: sd.problem-breakdowns.job-scheduler.notes
type: qa
step: 11
---
## Q
**分布式任务调度器 · 深入三：可见失败与重试退避**｜摘要 · 必会

作业失败有哪两种？任务代码抛异常时怎么重试？

## A
- **两种失败：**
  - 可见失败：任务代码有 bug 或参数不对，作业明显失败了；
  - 不可见失败：worker 自己宕机了，没人报告。
- **可见失败的处理：** 用 try/catch 包住任务代码，记录错误并标记失败；重试几次（比如 3 次），每次指数退避，用尽后标记 FAILED 不再重试。
- **具体做法：**
  - 失败时把 Executions 状态更新为 RETRYING 并记尝试次数；
  - 把作业重新放进 SQS，延迟随次数增长，比如 5、25、125 秒，用重新入队时的 DelaySeconds 参数和尝试次数计算；
  - 3 次后仍失败，标记 FAILED。
- **SQS 提供的积木：** 可见性超时让失败消息重新出现；ApproximateReceiveCount 属性追踪重试次数；死信队列收集超过重试上限的消息。退避的计时逻辑要在 worker 代码里自己写。
