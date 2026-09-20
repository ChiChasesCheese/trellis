---
nodes: [problems.social.chat-messaging]
url: https://algomaster.io/learn/system-design-interviews/design-whatsapp
tags: [no-archive]
---
# Design WhatsApp | Algomaster
值得读：结构接近 Alex Xu 一书，用 Cassandra 存消息、PostgreSQL 存关系数据，明确提出"每收件人一行送达状态"而非复制消息体，也讨论了多设备同步和推送通知的角色。与本题解的分歧：本题解把这个存储切分决定量化到具体字节数（群聊放大约 8 倍存储），并补充了热分区的真实案例，而该文只停留在定性描述。

%% trellis:begin %%
## Source
[Open the original ↗](https://algomaster.io/learn/system-design-interviews/design-whatsapp)
%% trellis:end %%
