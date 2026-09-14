---
id: correctness-balance-derivation
node: correctness.ledger
type: qa
---
## Q
If balance = SUM(entries), how do you make balance reads fast AND enforce "no overdraft" under concurrent spends?

## A
- **Fast reads**: periodic **snapshots/checkpoints** — persist balance as of entry N; current balance = snapshot + entries since N. The snapshot is a cache, always rebuildable from entries.
- **Overdraft enforcement** needs the check and the append to be atomic per account:
  - serialize per account (row lock on an account record, or single-writer per account partition), or
  - maintain a materialized balance updated **in the same transaction** as the entry insert, with a `CHECK (balance >= 0)` constraint.
- Distinguish **available vs posted** balance: holds/authorizations reduce available immediately, posted only on capture — most "double spend" bugs are really available-balance bugs.

## Q zh
如果 balance = SUM(entries)，如何既能让 balance 读取快速，又在并发消费时强制"禁止透支"？

## A zh
- **快速读取**：定期**快照/检查点** — 持久化第 N 个 entry 时的 balance；当前余额 = 快照 + 快照之后的 entry。快照是缓存，始终可以从 entry 重建。
- **禁止透支**需要检查和追加对每个账户原子性：
  - 按账户序列化（对账户记录加行锁，或单个写入器每账户分区），或
  - 维护物化 balance，在与 entry 插入**同一事务**中更新，带有 `CHECK (balance >= 0)` 约束。
- 区分**可用余额 vs 已过账**：冻结/授权立即减少可用额度，过账仅在交割时减少 — 大多数"双重花费"bug 其实是可用余额 bug。
