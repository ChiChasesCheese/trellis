---
id: hi-ov-whatsapp-2-options
node: sd.problem-breakdowns.whatsapp
type: qa
step: 2
tags: [通览]
---
## Q
**即时通讯 · 高层设计**｜通览

即时通讯的高层设计怎么搭？每个功能需求走哪条路径？

## A
**组件。** 客户端、L4 负载均衡、聊天服务器、DynamoDB、Redis Pub/Sub、对象存储。

**每条路径。**
- **建群：** 客户端经 WebSocket 发建群命令；服务器写一条 Chat 和每个成员各一条 ChatParticipant，返回 chatId。
- **收发消息：** 发送者发命令；服务器查成员，先写 Message 和每个收件人的 Inbox，回成功，再推给在线成员；多台服务器时经 Pub/Sub 转发。
- **离线补收：** 离线者的 Inbox 条目留在库里；上线后按 Inbox 取消息推送，客户端 ack 后删除，表设 TTL 过期。
- **收发媒体：** 客户端拿预签名 URL 直传对象存储，聊天服务器只转发附件地址；接收方同样凭预签名 URL 取。

**存储。** DynamoDB 存 Chat、ChatParticipant、Message、Inbox，键值访问快、好扩展；成员表另建以 participantId 为键的二级索引，两个方向都能查。附件字节放对象存储，数据库不擅长大文件。
