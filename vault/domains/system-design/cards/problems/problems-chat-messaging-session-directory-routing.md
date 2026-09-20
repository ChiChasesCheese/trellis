---
id: problems-chat-messaging-session-directory-routing
node: problems.social.chat-messaging
type: qa
step: 3
tags: [grown]
---
## Q
In a chat system where a sender's and a recipient's WebSocket connections can land on different gateway servers, why is a centralized session directory (e.g. Redis mapping user/device to gateway) usually preferred over giving every user a dedicated Kafka topic for cross-gateway routing?

## A
A session directory only stores a lookup record — which gateway currently holds a given user's socket, tens of bytes per online user — so it stays small and fast even at a billion online users. Giving every user a dedicated Kafka topic fails for a structural reason: every topic-partition costs the cluster file handles, index files, replication state and controller metadata, and Kafka's control plane is built for thousands to low millions of partitions, not a billion. So routing is kept as a cheap 'who is online where' lookup, separate from any durable delivery queue used for offline fan-out.

## Q zh
在一个聊天系统中，发送方和接收方的 WebSocket 连接可能落在不同的网关服务器上，为什么跨网关路由通常选择一个集中式会话目录（例如 Redis 存储用户/设备到网关的映射），而不是为每个用户建一个专属的 Kafka 主题？

## A zh
会话目录只存一条查找记录——某个用户当前的连接在哪台网关，每个在线用户仅占几十字节——所以即使十亿在线用户规模也依然很小很快。为每个用户建一个专属 Kafka 主题在结构上就行不通：每个主题分区都要占用文件句柄、索引文件、复制状态和控制器元数据，而 Kafka 的控制面是为几千到几百万个分区设计的，不是十亿个。所以路由被保持为一个廉价的「谁在哪」查找，和用于离线扇出的持久化投递队列是分开的。
