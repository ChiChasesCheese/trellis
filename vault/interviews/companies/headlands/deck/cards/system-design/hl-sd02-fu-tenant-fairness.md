---
id: hl-sd02-fu-tenant-fairness
node: system-design.sd02-job-scheduler
type: qa
step: 37
---
## Q
追问：多租户公平，一个租户提交了一亿个任务怎么办？

## A
提交时按租户限流 + 配额；到期出轮后按租户分队列，加权公平分发（WFQ / DRR）；每个租户有「最大同时到期数」阈值，超出的任务视为 lateness 归因于租户自身；监控按租户的 lateness。

可以说：「调度器的公平性不在时间轮，而在出轮之后的分发队列。」
