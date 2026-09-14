---
id: delivery-rollback-forward-or-back
node: delivery.rollback
type: qa
---
## Q
A new writer has emitted metadata the old reader cannot parse. Is rollback still the safest response?

## A
Not automatically. Rolling back the reader may deepen the outage if incompatible state already exists. Freeze further writes, quantify affected state, and choose among a compatibility shim, roll-forward fix, or restoring versioned data. This is why releases should use expand-contract and backward-readable formats: operational rollback must remain a valid transition, not a wish.

## Q zh
新 writer 已经写出旧 reader 无法 parse 的 metadata。rollback 仍然是最安全响应吗？

## A zh
不一定。如果 incompatible state 已存在，回退 reader 可能扩大 outage。应冻结后续 write、量化 affected state，再在 compatibility shim、roll-forward fix 或恢复 versioned data 之间选择。这正是 release 应使用 expand-contract 和 backward-readable format 的原因：operational rollback 必须是有效 transition，而不是愿望。
