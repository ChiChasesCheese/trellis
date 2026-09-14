---
id: correctness-saga-orchestrator-recovery
node: correctness.saga
type: qa
---
## Q
The saga orchestrator crashes mid-workflow. What must have been persisted for safe resume, and how are the resulting duplicates and silences handled?

## A
The orchestrator is a **persistent state machine**: it durably records the saga instance + current step *before* dispatching each command (its own DB write + command via outbox — the orchestrator has its own dual-write problem).

On resume, it re-reads state and re-dispatches the in-flight step, so:
- **Duplicates**: every participant command carries a deterministic id (`saga_id:step`) and participants are idempotent consumers.
- **Silence** (reply lost or participant down): per-step **timeouts** drive the state machine into retry or compensation — a saga must never wait forever.

This is exactly what workflow engines (Temporal) give you off the shelf: durable step state + deterministic replay, so you don't hand-roll the recovery matrix.

## Q zh
saga orchestrator 在工作流中崩溃。什么必须持久化以安全恢复，结果的重复和沉默怎样处理？

## A zh
orchestrator 是**持久状态机**：在分派每个命令前耐久记录 saga 实例 + 当前步（其自己的 DB 写 + 经 outbox 的命令 — orchestrator 有其自己的双写问题）。

恢复时，它重读状态和重新分派在途步，所以：
- **重复**：每个参与者命令携带确定性 id（`saga_id:step`），参与者是幂等消费者。
- **沉默**（回复丢失或参与者故障）：每步**超时**驱动状态机进入重试或补偿 — saga 绝不能永远等待。

这正是工作流引擎（Temporal）现成给你的：耐久步状态 + 确定性重放，不用手工推导恢复矩阵。
