---
id: async-event-sourcing-vs-cdc
node: async.streaming.cdc
type: qa
---
## Q
Event sourcing and CDC both give you "a stream of changes." What is the fundamental distinction, and when do you pick each?

## A
- **Event sourcing**: domain events (`OrderCancelled`) are the **source of truth**, written first, expressing *intent*; current state is a derived projection. The application must be designed around it — replay, versioned event schemas, projections.
- **CDC**: the mutable database stays the source of truth; the stream is a **derived byproduct** of row changes (`UPDATE orders SET status=...`), capturing *effect* without intent, and leaking the table schema as your public contract.

Pick CDC to bolt streaming onto an **existing** CRUD system with zero app changes; pick event sourcing when the domain needs **intent-level history and audit** (ledgers, workflow). Middle path: keep CRUD + publish explicit events via an outbox ([[correctness-outbox-mechanism]]).

## Q zh
事件溯源和 CDC 都给你"一个变化流"。根本区别是什么，何时选择每种？

## A zh
- **事件溯源**：领域事件（`OrderCancelled`）是**真实来源**，首先被写入，表达*意图*；当前状态是派生的投影。应用必须围绕它设计 — replay、版本化的事件 schema、投影。
- **CDC**：可变数据库保持真实来源；流是行变化的**派生副产品**（`UPDATE orders SET status=...`），捕获*效果*而不是意图，泄露表 schema 作为你的公开契约。

选择 CDC 来**已有** CRUD 系统零应用改动地添加流；当领域需要**意图级别的历史和审计**（账本、工作流）时选择事件溯源。中间路径：保持 CRUD + 通过 outbox 发布显式事件。
