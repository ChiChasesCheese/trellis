---
id: problems-email-service-attachment-dominates-storage
node: problems.media.email-service
type: qa
step: 1
tags: [grown]
---
## Q
In a Gmail-class email service design where attachments are stored content-addressed (deduplicated by content hash) in object storage separately from message metadata in a wide-column store, capacity math shows new attachment bytes accumulate at roughly 9x the rate of new metadata bytes per year. What design decision does this ratio force, and why does modeling attachment dedup off *sent* events rather than *received* copies matter?

## A
The ratio forces attachments to be treated as the dominant storage cost driver: they must live in object storage with content-addressed deduplication, not inline in the same row as message metadata, because that's where nearly 90% of new storage growth comes from. Modeling dedup off sent events (rather than received copies) matters because a single send event with N recipients (via CC or a mailing list) produces byte-identical attachment content for every recipient — deduplicating at the point of sending means the attachment is stored once regardless of how many mailboxes reference it, while deduplicating only per-received-copy would miss this and massively overcount unique bytes, since the same physical bytes would otherwise appear to be N separate pieces of content.

## Q zh
在一个 Gmail 级邮件服务设计中，附件以内容寻址（按内容哈希去重）方式存在对象存储里，和存在宽列存储里的消息元数据分开存放。容量估算显示，新增附件字节的年增长速度大约是新增元数据字节的 9 倍。这个比例逼出了什么设计决策？为什么要按「发送事件」而不是「收件副本」来建模附件去重？

## A zh
这个比例迫使附件被当作主导存储成本的因素来处理：它们必须存在带内容寻址去重的对象存储里，而不是和消息元数据同一行内联存放，因为新增存储增长里将近九成来自附件。按发送事件（而不是收件副本）建模去重之所以重要，是因为一次有 N 个收件人的发送事件（通过抄送或邮件列表）会为每个收件人产生字节完全相同的附件内容——在发送这个时间点去重，意味着不管有多少个邮箱引用它，这份附件只存一份；如果只按收件副本各自去重，就会漏掉这一点，严重高估唯一字节数，因为同样的物理字节本来会被当成 N 份独立内容。
