---
id: correctness-saga-orchestration-choreography
node: correctness.saga
type: qa
---
## Q
Orchestrated vs choreographed saga: how does each work, and when do you pick which?

## A
- **Choreography**: each service reacts to the previous service's events (order-created → payment listens → payment-charged → inventory listens). No central brain. Fine for **2–3 steps**; beyond that the workflow exists nowhere — you can't see state, and compensation paths sprawl across services.
- **Orchestration**: a coordinator (state machine, often Temporal/Step Functions) commands each step and drives compensations on failure. Workflow state is explicit, observable, and testable; the orchestrator is extra infra and a dependency.

Pick orchestration for anything money-shaped or with >3 steps; the "orchestrator = single point of failure" worry is solved by persisting its state and making step handlers idempotent.

## Q zh
编排 vs 编舞 saga：各怎样工作，什么时候选哪个？

## A zh
- **编舞**：每个服务对前一服务的事件反应（order-created → payment 监听 → payment-charged → inventory 监听）。无中心大脑。适合**2-3 步**；超过这个工作流无处存在 — 你看不到状态，补偿路径遍布服务。
- **编排**：协调器（状态机，常用 Temporal/Step Functions）命令每步并在失败时驱动补偿。工作流状态显式、可观察、可测试；orchestrator 是额外基础设施和依赖。

任何钱相关或 >3 步选编排；「orchestrator = 单点故障」的担忧通过持久化其状态和幂等步骤处理器解决。
