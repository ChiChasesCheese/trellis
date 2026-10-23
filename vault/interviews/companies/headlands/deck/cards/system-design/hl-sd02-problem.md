---
id: hl-sd02-problem
node: system-design.sd02-job-scheduler
type: qa
step: 1
---
## Q
设计题：未来时刻任务调度器。调用方提交一次性任务并指定未来时刻 `fireAt`，服务要持久化并在 `fireAt` 之后的有界延迟 Δ 内触发，支持取消。题面里 one-time、durable、future-time、bounded delay 四个词各带来什么设计后果？

## A
- **one-time**：不是 cron / 周期任务，一个任务只触发一次、生命周期短；周期任务可归约成「触发后再调度下一次」；
- **durable**：提交成功返回后即使整机崩溃也不丢，所以先写日志再确认，崩溃恢复要能重建；
- **future-time**：触发时刻在未来，范围可能从秒到年，近期与远期要用不同结构（时间轮 + 分层存储）；
- **bounded delay**：触发时间 ∈ [fireAt, fireAt + Δ]，不早、不过晚；SLO 要量化，时钟、突发（thundering herd）、故障切换都要算进 Δ。

需要描述：数据模型、触发机制、故障恢复，以及如何保证有界延迟和「不丢 / 不重（或明确重复语义）」。
