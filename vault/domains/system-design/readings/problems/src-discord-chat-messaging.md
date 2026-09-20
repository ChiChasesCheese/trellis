---
nodes: [problems.social.chat-messaging]
url: https://discord.com/blog/how-discord-stores-trillions-of-messages
tags: [engineering-blog]
---
# How Discord Stores Trillions of Messages
值得读：Discord 官方工程博客记录了消息存储从 12 个 Cassandra 节点到 177 个节点、再迁移到 72 个 ScyllaDB 节点的真实过程，包含热分区成因（大频道写入量远超普通频道导致 quorum 读写拖慢整个集群）、GC 停顿的运维代价、以及迁移前后的 P99 延迟对比（读 40–125ms→15ms，写 5–70ms→稳定 5ms）。本题解的"瓶颈、故障与演进"一节直接引用这组数字作为热分区问题的真实证据，而多数面试向文章只泛泛提"按分区键分片"而不给出量化后果。

%% trellis:begin %%
## Source
[Open the original ↗](https://discord.com/blog/how-discord-stores-trillions-of-messages)

## Archived copy
![[src-discord-chat-messaging-clip]]
%% trellis:end %%
