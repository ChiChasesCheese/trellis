---
id: problems-digital-wallet-heavy-account-snapshot-cadence
node: problems.commerce.digital-wallet
type: qa
step: 6
tags: [grown]
---
## Q
In an event-sourced digital wallet, a heavy user making 20 transfers/day accumulates about 73,000 balance-affecting events over 5 years (20 × 365 × 5 × 2, two events per transfer for the sending side). Why does this number force a snapshot strategy rather than always replaying from the start?

## A
If every balance read replayed the account's full event history, read latency would grow roughly linearly with account age and activity — a 5-year-old heavy account's query would already be replaying 73,000 events, and the number only grows for as long as the account stays active. The fix is a periodic snapshot: the balance is persisted every N events (this design uses every 500), and a read becomes the latest snapshot plus replay of only the events since — the snapshot itself is disposable and always reconstructible from the full event history, so it never becomes a second source of truth.

## Q zh
在一个事件溯源的数字钱包中，一个日均 20 笔转账的重度用户 5 年内会累积约 73,000 个影响余额的事件（20 × 365 × 5 × 2，发送方每笔转账 2 个事件）。为什么这个数字迫使系统必须采用快照策略，而不能永远从头重放？

## A zh
如果每次读余额都要重放账户的完整事件历史，读延迟会随账户年龄和活跃度大致线性增长——一个 5 年的重度账户查询届时已经要重放 73,000 个事件，而且只要账户保持活跃，这个数字还会继续增长。解法是定期打快照：每 N 个事件持久化一次余额（本设计取 500），读取变成“最近快照 + 快照之后的事件重放”——快照本身是可丢弃的，随时可以从完整事件历史重新计算，因此它永远不会变成第二份权威数据源。
