---
id: hi-c-sd-temporal-b03-activity-semantics
node: sd.deep-dives.temporal.beyond
type: qa
step: 3
---
## Q
**Temporal · Activity 的超时、重试与心跳**｜拓展 · 加分

Activity 有哪几种超时？重试策略怎么配？长时间 Activity 怎么避免被误判为失败？

## A
- **超时有几种：** 排队等待 worker 的时间（schedule-to-start）、单次执行的时间（start-to-close）、含重试在内的总时间（schedule-to-close）。至少要设置执行超时，否则 worker 卡死时无人知道。
- **重试策略：** 默认会重试，带指数退避，可设最大次数、最大间隔；对不该重试的错误（参数非法、业务拒绝）标记为不可重试，让 Workflow 走失败分支，而不是无意义地重试。
- **心跳（heartbeat）：** 长时间的 Activity（大文件处理）定期发心跳，表示还活着，也可带上进度；worker 崩溃时心跳停止，Temporal 很快发现并重试，下一次可以从心跳里的进度继续。
- **含义：** 至少一次的执行语义，加上这些超时，决定了 Activity 必须幂等，并保持单次执行足够短或带心跳。
