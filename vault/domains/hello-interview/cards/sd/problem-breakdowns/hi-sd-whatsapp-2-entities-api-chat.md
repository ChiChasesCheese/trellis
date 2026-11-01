---
id: hi-sd-whatsapp-2-entities-api-chat
node: sd.problem-breakdowns.whatsapp
type: qa
step: 2
---
## Q
**WhatsApp 的实体、WebSocket 接口与建群**｜系统设计 · 问题拆解

聊天系统的核心实体和接口怎么定？为什么不用 REST，而用 WebSocket 命令加客户端确认（ack）？建群时 DynamoDB 的表和索引怎么设计，负载均衡用 L4 还是 L7？

## A
**要点。** 实体：用户（User）、聊天（Chat，2 到 100 人）、消息（Message）、客户端（Client，一个用户可能有多台设备）。

**接口。** 聊天是双向高频更新，所以用 WebSocket（走 TLS），把接口定义为连接上的命令：`createChat`、`sendMessage`、`createAttachment`、`modifyChatParticipants`，服务端推给其他客户端的命令有 `chatUpdate`、`newMessage`。客户端收到命令必须回 ack，服务端才能确定消息真的到了客户端，不必重发，这是不丢消息的关键。

**建群的数据设计。** Chat 表以 chatId 为主键。ChatParticipant 表用复合主键：chatId 为分区键、participantId 为排序键，一次 Query 取出群成员；再建全局二级索引（GSI），participantId 为分区键、chatId 为排序键，用来查某用户的所有聊天。小群可一个 DynamoDB 事务写完（最多 100 条），接近 100 人时要分批。

**取舍。** 负载均衡用 L4 就够：只有 WebSocket 连接，不需要按路径或请求头路由，L4 性能更高。
