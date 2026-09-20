---
id: problems-chat-messaging-ten-x-evolution
node: problems.social.chat-messaging
type: qa
step: 8
tags: [grown]
---
## Q
In a chat system designed for 300 million DAU and 45 million peak concurrent connections, what has to change at 10x scale (3 billion DAU, ~450 million peak concurrent connections), and why does the presence subsystem need to change even though it seemed fine at the original scale?

## A
The gateway fleet scales roughly linearly, from around 600 to around 6,000 instances, because it is bound by concurrent connections rather than CPU. At this size a single global session directory becomes the new bottleneck, so it must shard by user-id range or region, with cross-region lookups proxied only when a conversation actually spans regions. The message store similarly moves from one global keyspace to per-region clusters with async cross-region replication for conversations that span regions, deliberately giving up global cross-region ordering (which was never required — only per-conversation order was). Presence has to tighten further to a strict subscribe-to-open-chats model, because any lingering broadcast-style fan-out that was merely expensive at 45 million concurrent users becomes architecturally impossible at 450 million.

## Q zh
在一个为 3 亿日活、峰值 4500 万并发连接设计的聊天系统中，扩展到 10 倍规模（30 亿日活，约 4.5 亿峰值并发连接）时哪些部分必须改变？为什么 presence（在线状态）子系统即使在原规模下看起来没问题，也必须进一步改变？

## A zh
网关机群大致线性扩展，从约 600 台增长到约 6000 台，因为它受并发连接数而非 CPU 限制。在这个规模下，单一的全局会话目录会成为新的瓶颈，因此必须按用户 ID 区间或地域分片，只有当一个会话确实跨地域时才代理查询对方地域。消息存储同样从单一全局 keyspace 演变为按地域独立的集群，对跨地域会话做异步复制，主动放弃跨地域的全局顺序保证（这本来就不是需求——只需要会话内有序）。presence 必须进一步收紧为严格的「仅订阅当前打开会话」模型，因为任何在 4500 万并发时只是「代价较高」的残留广播式扇出，在 4.5 亿规模下会在架构上直接不可行。
