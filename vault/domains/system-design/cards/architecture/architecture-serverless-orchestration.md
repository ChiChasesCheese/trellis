---
id: architecture-serverless-orchestration
node: architecture.serverless
type: qa
---
## Q
A workflow (order → charge → fulfill → notify) takes hours and must survive crashes, but FaaS functions cap at ~15 minutes and keep no state. What's the pattern?

## A
**Durable workflow orchestration** (Step Functions, Temporal, Durable Functions): the workflow's *state machine* lives in the orchestrator's durable store, and each step runs as a short, **idempotent** function invocation. The orchestrator persists progress after every step, so a crash resumes from the last completed step — never holding state in a long-running process.

This also gives you retries with backoff per step, timers ("wait 3 days"), and compensation hooks — effectively managed **saga** execution.

Contrast with **choreography** (functions chained via events): fine for 2–3 steps, but end-to-end state becomes invisible and error handling scatters — orchestrate once a human needs to answer "where is order 123 stuck?"

## Q zh
一个工作流（订单 → 收费 → 履行 → 通知）耗时数小时并必须生存崩溃，但 FaaS 函数上限 ~15 分钟并保持无状态。什么是模式？

## A zh
**持久工作流编排**（Step Functions、Temporal、Durable Functions）：工作流的*状态机*在编排器的持久存储中生活，每个步运行作为短、**幂等**函数调用。编排器在每一步后坚持进度，所以崩溃从最后完成的步恢复——永不在长期运行过程中保持状态。

这也给你每步重试与退避、计时器（"等等 3 天"）和补偿钩子——有效管理**saga**执行。

与**choreography**（函数通过事件链）对比：对 2–3 步够用，但端到端状态变得不可见，错误处理分散——一旦有人需要回答"订单 123 卡在哪一步？"，就该改用 orchestration。
