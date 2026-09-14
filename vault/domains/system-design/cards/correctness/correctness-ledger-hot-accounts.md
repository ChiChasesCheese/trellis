---
id: correctness-ledger-hot-accounts
node: correctness.ledger
type: qa
---
## Q
A platform fee account appears in every transaction — millions of entries/day against one ledger account. Why does it melt down, and how do you design around it?

## A
If posting maintains a materialized balance row, every transaction serializes on that **one row lock** — the fee account becomes a global throughput ceiling.

- **Don't maintain a synchronous balance** for it: append entries lock-free; derive the balance **asynchronously** (projection / snapshot + delta, [[correctness-balance-derivation]]). Legit because internal omnibus/fee accounts have no overdraft rule to enforce at write time.
- If a balance constraint IS required: **shard into sub-accounts** (fee-01..fee-32, hash-routed), each with its own serialization; report SUM across shards.
- Reserve synchronous check-and-post for accounts where overdraft actually matters (customer wallets).

Interview line: hot accounts are why "row-lock the balance" doesn't survive scale — pick per-account strategy by its invariant.

## Q zh
平台费账户出现在每笔交易中 — 每天百万条分录针对一个账本账户。为什么它会熔断，怎样设计来规避？

## A zh
如果过账维护物化 balance 行，每笔交易在那**唯一行锁**上序列化 — 费账户成全局吞吐量天花板。

- **不维护它的同步 balance**：追加分录无锁；**异步**推导 balance（投影 / 快照 + 增量，[[correctness-balance-derivation]]）。这合理是因为内部 omnibus/费账户在写入时没有要强制的禁止透支规则。
- 如果 balance 约束**确实**需要：**分片成子账户**（fee-01..fee-32，哈希路由），各自序列化；跨分片报 SUM。
- 预留同步检查-过账给禁止透支真的重要的账户（客户钱包）。

面试金句：热账户是为什么"行锁 balance"无法扩展的原因 — 按账户的不变量选择策略。
