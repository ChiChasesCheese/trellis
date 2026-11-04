---
id: hi-sd-whatsapp-3-send-inbox
node: sd.problem-breakdowns.whatsapp.exam
type: qa
step: 3
---
## Q
**WhatsApp 的发消息与离线收件箱**｜系统设计 · 问题拆解

先假设只有一台聊天服务器（Chat Server），消息要怎么发才能同时支持在线实时投递和离线 30 天补收？Inbox 表怎么用，写入量大概多少？

## A
**要点。** 单机起步先把机制想清楚，再谈扩展。服务器用内存哈希表保存 userId 到 WebSocket 连接的映射。

**发送流程。**
1. 发送方发 `sendMessage`
2. **查成员得收件人：** 服务器查 ChatParticipant 得到所有成员
3. 把消息写入 Message 表，并给每个接收者在 Inbox 表写一条
4. 向发送方返回成功和 messageId
5. 对在线的接收者推 `newMessage`；客户端回 ack 后，服务器删掉对应 Inbox 条目

离线用户的 Inbox 条目保留。他重新连接时：查 Inbox 得到未送达的消息 ID，到 Message 表取内容，推送，收到 ack 后删除。Message 和 Inbox 都设 TTL 到期清理。

**数字。** 假设 2 亿活跃用户、人均每天 20 条：40 亿条/天，约 4 万条/秒。1:1 聊天每条写一次 Message 加一次 Inbox，计入群聊后约 10 万次写入/秒，以 userId 为分区键，DynamoDB 完全承受得了。
