---
id: problems-chat-messaging-group-fanout-storage-model
node: problems.social.chat-messaging
type: qa
step: 2
tags: [grown]
---
## Q
In a group chat system, why is storing one copy of the message body plus a narrow per-recipient delivery-status row cheaper than copying the full message body into every recipient's inbox, and by roughly how much at scale?

## A
If 15% of 15 billion daily messages go to groups averaging 9 other recipients, duplicating a ~200-byte message body per recipient adds about 4.05 TB/day of extra storage and write volume. Adding instead a ~25-byte status row (message_id, user_id, status, timestamp) per recipient adds only about 506 GB/day — roughly an 8x storage saving — because the message body is written exactly once per conversation regardless of how many people are in the group, and only the small per-recipient status rows scale with group size.

## Q zh
在一个群聊系统中，为什么只存一份消息体、再为每个收件人存一行窄的送达状态记录，会比把完整消息体复制进每个收件人的信箱更省空间？在这个规模下大约省多少？

## A zh
假设 150 亿条日消息中有 15% 发到群组，平均群大小为 10 人（9 个其他收件人），若为每个收件人复制一份约 200 字节的消息体，会额外增加约 4.05TB/天的存储与写入量；而只为每个收件人增加一行约 25 字节的状态记录（message_id、user_id、status、timestamp），只增加约 506GB/天——大约省 8 倍存储——因为消息体无论群多大都只写一次，只有很小的每收件人状态行会随群规模线性增长。
