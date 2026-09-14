---
id: architecture-microservices-tax
node: architecture.services
type: qa
---
## Q
Name the operational bill that arrives with microservices — the things a monolith gave you for free.

## A
- **In-process call → network call**: latency, partial failure, timeouts/retries/circuit breakers on every edge; a deep call graph multiplies tail latency and failure probability.
- **Debugging becomes distributed tracing**: no single stack trace or debugger; you need correlation ids, centralized logging, and tracing infra just to answer "what happened".
- **Transactions become sagas/outboxes**: cross-entity consistency stops being `BEGIN...COMMIT`.
- **Deploy/testing surface explodes**: N pipelines, version-compatibility matrices, contract tests, per-service on-call.

The senior framing: microservices trade **development-time coupling** for **runtime and operational complexity** — worth it only when the org-scaling benefit outweighs this bill.

## Q zh
命名随微服务而来的操作账单——一个整体免费给你的东西。

## A zh
- **进程内调用 → 网络调用**：延迟、部分故障、每边上的 timeout/retry/circuit breaker；深调用图乘以尾延迟和故障概率。
- **调试变成分布式跟踪**：无单栈跟踪或调试器；你需要相关 id、集中日志和跟踪基础设施只是回答"发生了什么"。
- **事务变成 saga/outbox**：跨实体一致性停止`BEGIN...COMMIT`。
- **部署/测试表面爆炸**：N 管道、版本兼容性矩阵、契约测试、每个服务待命。

高级框架：微服务贸易**开发时耦合**对**运行时和操作复杂性** ——仅当组织缩放好处超过这个账单时值得。
