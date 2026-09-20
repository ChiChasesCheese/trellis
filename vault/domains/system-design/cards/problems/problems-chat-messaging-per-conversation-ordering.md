---
id: problems-chat-messaging-per-conversation-ordering
node: problems.social.chat-messaging
type: qa
step: 4
tags: [grown]
---
## Q
In a chat system, why does assigning each message a monotonically increasing sequence number scoped to a single conversation (rather than a global sequence or client wall-clock timestamps) solve ordering without a separate coordination service?

## A
All writes for one conversation already have to land on the same storage partition so that time-range queries and history scrolling work, so that partition can hand out a strictly increasing per-conversation `seq` as a free side effect of being the single writer for that conversation — no extra coordination service is needed. This only guarantees order within a conversation, not across different conversations, which matches what chat users actually care about. Client wall-clock timestamps are avoided because clock drift between devices routinely causes visible reordering.

## Q zh
在一个聊天系统中，为什么给每条消息分配一个限定在单个会话内的单调递增序号（而不是全局序号或客户端墙钟时间戳）能在不引入额外协调服务的情况下解决顺序问题？

## A zh
一个会话的所有写入本来就必须落到同一个存储分区（否则按时间范围查询和历史滚动加载都做不到），所以该分区作为该会话唯一的写入者，可以顺带分配严格递增的会话内 `seq`，不需要额外的协调服务。这只保证会话内有序，不保证跨不同会话有序，这恰好符合聊天用户真正关心的东西。客户端墙钟时间戳被避免使用，因为设备间的时钟漂移经常导致明显的乱序。
