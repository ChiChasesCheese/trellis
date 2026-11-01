---
id: hi-pt-messenger-chat-system-4-send-flow
node: qb.sd.messenger-chat-system.points
type: qa
step: 4
---
## Q
**聊天与即时通讯系统 · 发送流程与收件箱**｜出自：聊天与即时通讯系统 › 整体设计

聊天服务收到 `sendMessage` 后按什么顺序处理？收件箱存什么？

## A
**顺序。** 用 `(chatId, clientMsgId)` 去重 → 分配会话内 `seq` → 消息库写一次（正文只存一份）→ 给每个收件人每台设备写一条收件箱指针（只含 `chatId`、`seq`，几十字节）→ 写成功才回「已发送」。
**确认。** 客户端 `ack` 后删收件箱条目并回「已送达」，打开会话后再发「已读」。
