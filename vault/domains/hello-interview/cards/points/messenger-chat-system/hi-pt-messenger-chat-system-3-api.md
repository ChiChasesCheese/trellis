---
id: hi-pt-messenger-chat-system-3-api
node: qb.sd.messenger-chat-system.points
type: qa
step: 3
---
## Q
**聊天与即时通讯系统 · WebSocket 接口与幂等键**｜出自：聊天与即时通讯系统 › 核心实体与接口

聊天的发送接口怎么设计？为什么用 WebSocket？历史分页用 offset 还是游标？

## A
**发送。** `sendMessage {chatId, clientMsgId, text, attachments}`，`clientMsgId` 由客户端生成，是幂等键；`ack` 客户端确认后服务端才删收件箱条目；`sync {cursor}` 重连补发。
**协议。** 高频双向推送用 WebSocket，REST 轮询太贵。
**历史。** `GET .../messages?before=<seq>`，用游标不用 offset，新消息会让 offset 漂移。媒体用预签名 URL 直传，消息里只放引用。
