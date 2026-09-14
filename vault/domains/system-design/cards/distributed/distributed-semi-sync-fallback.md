---
id: distributed-semi-sync-fallback
node: distributed.replication.leader
type: qa
---
## Q
Your team runs semi-synchronous replication (the leader waits for one follower's ack before acknowledging a commit) and advertises "zero data loss on failover". Name the ways that promise silently fails in practice.

## A
- **Silent degradation to async**: implementations keep availability when the sync follower stops responding — e.g. MySQL semi-sync commits anyway after a timeout and drops to fully async. The zero-loss guarantee evaporates *exactly during the incidents it was bought for*, unless you alert on the degraded state.
- **Ack means received, not applied**: the follower acknowledges once the change is durably in its relay/receive log, not once it's applied to tables. Durability holds, but reads on that follower still lag.
- **Failover must pick the right node**: zero loss only holds if promotion targets the follower that actually holds the acked writes — automation that promotes "any healthy follower" can still lose data.

Interview framing: semi-sync narrows the loss window; whether it *closes* it depends on the timeout policy and the failover selection logic, so state both.

## Q zh
你们团队使用半同步复制（semi-synchronous，leader 在确认提交前等待一个 follower 的 ack），并对外承诺"故障切换零数据丢失"。列举这个承诺在实践中悄悄失效的几种方式。

## A zh
- **无声降级为异步**：为了保住可用性，实现会在同步 follower 不响应时继续提交——例如 MySQL 的半同步在超时后照常提交并退化为完全异步。零丢失保证*恰好在它被买来应对的事故期间*蒸发，除非你对降级状态设置了告警。
- **Ack 只代表收到，不代表已应用**：follower 在变更持久写入它的 relay log/接收日志后就会 ack，而不是应用到表之后。持久性成立，但在这个 follower 上读仍然有滞后。
- **故障切换必须选对节点**：零丢失只在提升真正持有已 ack 写入的那个 follower 时成立——"提升任意一个健康 follower"的自动化仍可能丢数据。

面试表述：半同步收窄了丢失窗口；是否*彻底关闭*取决于超时策略和故障切换的选主逻辑，两者都要讲到。

