---
id: distributed-total-order-broadcast
node: distributed.consensus
type: cloze
---
Total order broadcast guarantees {{c1::reliable delivery (no message lost) and totally ordered delivery — every node sees the same messages in the same order}}; it is formally {{c2::equivalent to consensus — each position in the shared log is one consensus decision, so Raft/Paxos give you TOB and vice versa}}. You get linearizable compare-and-set/uniqueness on top of it by {{c3::appending your claim to the log, reading the log back, and winning only if your message is the first claim for that key — log position is the serial order}}. This log framing is why "replicated state machine", "Raft log", and "Kafka partition ordering" are the same idea at different fault-tolerance levels.

## zh
总序广播保证{{c1::可靠投递（不丢消息）和完全有序的投递——每个节点以相同的顺序看到相同的消息}}；它在形式上{{c2::等价于共识——共享日志中的每一个位置就是一次共识决策，所以 Raft/Paxos 能给你总序广播，反过来也一样}}。在它之上实现线性一致的 compare-and-set/唯一性约束的方法是{{c3::把你的申领追加到日志中，再把日志读回来，只有当你的消息是该 key 的第一条申领时才算赢——日志位置就是序号}}。正是这种"日志"框架，让"复制状态机"、"Raft 日志"、"Kafka 分区顺序"在不同容错级别上其实是同一个想法。
