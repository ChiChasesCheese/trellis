---
id: distributed-raft-guarantees
node: distributed.consensus
type: qa
---
## Q
What does Raft actually guarantee about leaders and logs, and what mechanism enforces each guarantee?

## A
- **Election safety**: ≤1 leader per term — each node votes once per term, and a candidate needs a **majority**; two majorities always intersect.
- **Leader completeness**: an elected leader already holds every committed entry — voters **refuse candidates whose log is less up-to-date** than theirs (compare last term, then length), so a majority-committed entry exists on at least one voter of any winning majority.
- **Log matching / state machine safety**: if two logs agree on an entry's index+term, they agree on everything before it (AppendEntries consistency check), so all nodes apply the same commands in the same order.

Consequence worth stating: entries flow only leader → follower; a new leader never overwrites committed entries, only uncommitted divergence.

## Q zh
Raft 对 leader 和日志到底保证了什么？每一条保证又是靠什么机制强制执行的？

## A zh
- **选举安全（election safety）**：每个任期最多 1 个 leader——每个节点每个任期只投一次票，候选人需要**多数票**；任何两个多数派必然相交。
- **leader 完整性（leader completeness）**：选出的 leader 已经拥有所有已提交的条目——投票者会**拒绝日志不如自己新的候选人**（先比较最后一条的任期，再比较长度），所以任何一个获胜多数派中，至少有一个投票者持有每一条已被多数提交的条目。
- **日志匹配 / 状态机安全（log matching / state machine safety）**：如果两个日志在某个索引+任期上一致，那么它们在这条之前的所有内容也一致（靠 AppendEntries 的一致性检查保证），所以所有节点按相同顺序应用相同的命令。

值得一提的推论：条目只沿 leader → follower 方向流动；一个新 leader 永远不会覆盖已提交的条目，只会覆盖未提交的分歧部分。
