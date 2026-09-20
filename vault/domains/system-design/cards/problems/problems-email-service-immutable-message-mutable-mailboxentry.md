---
id: problems-email-service-immutable-message-mutable-mailboxentry
node: problems.media.email-service
type: qa
step: 2
tags: [grown]
---
## Q
In an email service's mailbox storage model, why is storing a message's content and its per-user state (read/unread, labels, starred) in the same row the wrong default, and what two-table split fixes it?

## A
Storing content and per-user state together means every high-frequency, small mutation — marking a message read is a change of a few bytes — forces a rewrite of a row that also contains the full message body, so write amplification scales with message size even though the actual change doesn't. The fix is to split into an immutable Message table (written once on receipt, holding the body and headers, never modified afterward) and a separate MailboxEntry table keyed by user, holding only a reference to the message plus mutable fields (flags, labels, thread id). Marking a message read then becomes a tens-of-bytes update to one MailboxEntry row that never touches the Message table, and listing an inbox becomes a range scan over MailboxEntry alone without reading any message bodies.

## Q zh
在一个邮件服务的邮箱存储模型里，为什么把一封信的内容和它的每用户状态（已读/未读、标签、星标）存在同一行是错误的默认做法？什么样的两表拆分能解决这个问题？

## A zh
把内容和每用户状态存在一起，意味着每一次高频、微小的改动——比如把一封信标记已读，只改动几个字节——都要重写一整行同时包含完整正文的记录，写放大和消息体大小成正比，即便实际改动的内容和消息体大小毫无关系。解决办法是拆成两张表：一张不可变的 Message 表（收到时只写一次，存正文和头部，之后永不修改），和一张按用户分区的 MailboxEntry 表（只存对消息的引用，加上可变字段：flags、标签、会话 id）。这样「标记已读」就变成对一行 MailboxEntry 做几十字节的更新，完全不碰 Message 表；「列出收件箱」也变成只在 MailboxEntry 上做一次范围扫描，不需要读取任何消息正文。
