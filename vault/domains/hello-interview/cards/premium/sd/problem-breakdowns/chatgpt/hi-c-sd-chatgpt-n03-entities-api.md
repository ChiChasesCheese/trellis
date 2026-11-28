---
id: hi-c-sd-chatgpt-n03-entities-api
node: sd.problem-breakdowns.chatgpt.notes
type: qa
step: 3
---
## Q
**ChatGPT · 实体与接口**｜摘要 · 必会

需要哪些核心实体？接口怎么设计，为什么 userId 不出现在请求里？

## A
- **实体：** User（含付费层，后面影响公平与调度）；Chat（一个对话线程，属于一个用户，含标题和时间戳）；Message（一轮发言：chatId、角色 user 或 assistant、内容、token 数）。后面深入时再加一个 Run，不在最初就出现。
- **接口：** `POST /chats` 返回 chatId；`POST /chats/{chatId}/messages` 带 `content` 发送提示词，朴素版直接返回完整回答；`GET /chats?cursor&limit` 列侧边栏对话；`GET /chats/{chatId}/messages?cursor&limit` 读一个对话的消息。
- **为什么游标分页：** 重度用户有成千上万个对话，长对话有上千条消息，一次全取太重。
- **身份：** userId 取自会话令牌或 JWT，每次请求在服务端校验对话归属；放在请求体里等于信任客户端，可被伪造。
