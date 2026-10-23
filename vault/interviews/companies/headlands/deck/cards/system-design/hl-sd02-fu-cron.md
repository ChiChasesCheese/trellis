---
id: hl-sd02-fu-cron
node: system-design.sd02-job-scheduler
type: qa
step: 36
---
## Q
追问：周期（cron）任务怎么支持？

## A
归约成一次性任务链：触发成功后（或触发时）按 cron 表达式计算下一次 `fireAt`，调度一个新的一次性任务；记录 `scheduleId` 与 `occurrence` 序号以保证幂等；错过的触发（宕机期间）的策略（补发全部 / 只补最近一次 / 跳过）要显式，由业务选择。

可以说：「周期任务 = 一次性任务 + 触发后调度下一次，不需要第二套机制。」
