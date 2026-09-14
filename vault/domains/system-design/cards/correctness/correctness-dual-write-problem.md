---
id: correctness-dual-write-problem
node: correctness.outbox
type: qa
---
## Q
A service commits to Postgres, then publishes an event to Kafka. Enumerate the failure modes of this "dual write" — and why wrapping both in try/catch doesn't fix it.

## A
- **Commit then crash before publish** → state changed, event lost; downstream never learns. (The common, silent one.)
- **Publish then commit fails** → phantom event for state that doesn't exist.
- **Retry the publish** after ambiguity → duplicates, and possibly out of order.

Try/catch can't help because there is **no atomic commit spanning two independent systems** — the broker doesn't participate in the DB transaction, and 2PC across DB + Kafka is impractical (broker support, blocking coordinator). The fix is to make the event part of the DB transaction: the transactional outbox.

## Q zh
服务先提交到 Postgres，再发布事件到 Kafka。列举这种"双写"的故障模式 — 为什么 try/catch 包装都无法修复？

## A zh
- **提交后崩溃再发布** → 状态已改，事件丢失；下游永不知晓。（常见的无声失败。）
- **发布后提交失败** → 状态不存在的幽灵事件。
- **歧义后重试发布** → 重复，可能乱序。

try/catch 无法帮助，因为**不存在跨两个独立系统的原子提交** — broker 不参与数据库事务，跨 DB + Kafka 的 2PC 不切实际（broker 支持、阻塞协调器）。修复方法是让事件成为数据库事务的一部分：事务型 outbox。
