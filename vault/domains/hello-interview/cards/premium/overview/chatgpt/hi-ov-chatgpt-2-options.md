---
id: hi-ov-chatgpt-2-options
node: sd.problem-breakdowns.chatgpt
type: qa
step: 2
tags: [通览]
---
## Q
**ChatGPT · 高层设计**｜通览

ChatGPT 的高层设计怎么搭？每个功能需求走哪条路径？

## A
**组件。** API 网关、无状态的聊天服务、推理服务（一组常驻模型的 GPU 机器）、Postgres。

**每条路径。**
- **发提示词得回答：** 客户端 POST 经网关到聊天服务，写用户消息，同步调推理服务取完整回答，写助手消息后返回；长回答可能空白 30 秒，也没有准入控制。
- **看历史并续聊：** 侧边栏和消息列表都读已有的表，游标分页；续聊时聊天服务把该对话全部历史拼在新消息前发给推理服务；对话过长会放不下，每轮也更贵。

**存储。** Postgres 的 chats 与 messages 表，都是按 chatId、userId 的简单行，选它只是合理默认。
