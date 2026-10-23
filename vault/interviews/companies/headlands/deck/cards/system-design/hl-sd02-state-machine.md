---
id: hl-sd02-state-machine
node: system-design.sd02-job-scheduler
type: qa
step: 11
---
## Q
任务的状态机有哪些状态和转换？重试怎么实现？

## A
状态：不存在 →(schedule)→ `SCHEDULED`；`SCHEDULED` →(cancel)→ `CANCELLED`（终态）；`SCHEDULED` →(到期出轮)→ `DISPATCHING`；`DISPATCHING` →(下游确认交付)→ `FIRED`（终态）；`DISPATCHING` →(交付失败，退避)→ 回到 `SCHEDULED`；超过重试上限 → `DEAD`（死信，告警）。

**重试 = 再调度**：失败后回到时间轮，`nextAttemptAt = now + backoff(attempt)`，复用同一个时间轮，不需要第二套机制。
