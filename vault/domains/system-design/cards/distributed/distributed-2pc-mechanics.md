---
id: distributed-2pc-mechanics
node: distributed.transactions.distributed
type: qa
---
## Q
Walk the two phases of 2PC and point at the exact commit point. Why can a participant that voted "yes" not simply time out and abort?

## A
1. **Prepare**: coordinator sends `prepare` with a global txid. Each participant does everything but commit — writes its changes and locks durably to its log — then answers **yes** (a promise it can commit under any subsequent crash) or **no**.
2. **Commit**: once all vote yes, the coordinator **writes its commit decision to its own durable log** — *that write is the commit point, and it is irrevocable*. Then it sends `commit`, retrying forever until every participant acknowledges.

A yes-voter can't unilaterally abort because it doesn't know whether the coordinator already reached the commit point: the `commit` message may simply be lost or delayed. If it aborted and the decision was commit, **atomicity is broken** — some participants committed, this one didn't. So it stays **in doubt**, holding its locks, blocking every conflicting transaction on that data, until the coordinator (or its recovered log) tells it the answer.

Worth adding: 3PC removes the block only under a synchronous network with reliable failure detection — assumptions real networks don't provide, which is why nobody ships it.

## Q zh
走一遍 2PC 的两个阶段，指出确切的提交点在哪里。为什么一个已经投票 "yes" 的参与者不能简单地超时就中止？

## A zh
1. **Prepare（准备）**：协调者带着全局 txid 发送 `prepare`。每个参与者做除提交之外的一切事——把变更和锁持久化写入自己的日志——然后回答 **yes**（承诺无论之后发生什么崩溃都能提交）或 **no**。
2. **Commit（提交）**：一旦所有人都投了 yes，协调者就**把提交决定写入自己的持久日志**——*这次写入就是提交点，且不可撤销*。然后它发送 `commit`，并不断重试直到每个参与者都确认。

一个投了 yes 的参与者不能单方面中止，因为它不知道协调者是否已经到达提交点：`commit` 消息可能只是丢失或延迟了。如果它中止了，而实际决定是提交，那**原子性就被打破**了——一些参与者提交了，这个没有。所以它保持**悬而未决（in doubt）**的状态，持有锁，阻塞该数据上所有冲突的事务，直到协调者（或其恢复的日志）告诉它答案。

值得补充：3PC 只有在同步网络、且故障检测可靠的前提下才能消除这种阻塞——而这些假设在真实网络中都不成立，这就是为什么没有人真正部署它。
