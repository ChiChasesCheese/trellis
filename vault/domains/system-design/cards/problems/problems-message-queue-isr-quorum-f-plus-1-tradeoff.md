---
id: problems-message-queue-isr-quorum-f-plus-1-tradeoff
node: problems.foundations.message-queue
type: qa
step: 3
tags: [grown]
---
## Q
In a Kafka-class message queue's ISR (in-sync replicas) replication model, why does tolerating f broker failures without losing committed data need only f+1 replicas, compared to the 2f+1 replicas a majority-quorum protocol (like Raft) needs for the same guarantee -- and what does this model give up in exchange?

## A
A majority-quorum protocol commits a write once more than half of all replicas acknowledge it, so it needs 2f+1 total replicas to guarantee f+1 of them (a majority) survive any f failures. The ISR model instead requires ALL currently in-sync replicas -- not a fixed majority -- to acknowledge before a write commits, so with f+1 replicas total, losing up to f of them still leaves at least one ISR member holding every committed message. The trade-off is that when the ISR shrinks to fewer members than the configured min.insync.replicas (for example, down to just the leader), the partition must choose between blocking acks=all writes until a replica catches back up (preserving durability, reducing availability) or letting an out-of-sync replica become leader anyway (unclean leader election, preserving availability at the risk of losing already-acknowledged data).

## Q zh
在一个 Kafka 一类消息队列的 ISR（in-sync replicas，同步副本集）复制模型里，为什么要容忍 f 个 broker 故障而不丢已提交数据，只需要 f+1 个副本，而不像多数派协议（如 Raft）那样需要 2f+1 个副本？这个模型换来这个优势的代价是什么？

## A zh
多数派协议要在超过半数副本确认后才算提交，所以需要总共 2f+1 个副本，才能保证任意 f 个故障后仍有 f+1 个（多数）存活。ISR 模型则要求当前全部同步副本（而不是固定的多数派）都确认之后才算提交，所以只要总共有 f+1 个副本，丢掉其中最多 f 个仍然至少有一个 ISR 成员持有全部已提交消息。代价是：当 ISR 收缩到少于配置的 min.insync.replicas 个成员时（比如只剩 leader 自己），该分区必须在「阻塞 acks=all 写入直到有副本重新追上」（保持持久性、牺牲可用性）和「让一个没追上的副本直接顶替成为 leader」（unclean leader election，保持可用性但可能丢失已确认的数据）之间做出选择。
