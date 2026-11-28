---
id: hi-c-sd-networking-essentials-x05-trust-body
node: sd.core-concepts.networking-essentials.exam
type: qa
step: 5
---
## Q
**网络基础 · 请求体里的用户 ID**｜考点 · 必会

接口 `GET /orders?user_id=...`，服务器直接用传入的 `user_id` 查订单，因为"已经走了 HTTPS，是安全的"。哪里错了？

## A
- **错在：** HTTPS 只保证传输中不被窃听和篡改，不保证请求内容是你的客户端生成的。攻击者改了 ID 就能读任意用户的数据。
- **做法：** 用户身份取自服务器验证过的会话或令牌，而不是请求里的字段；若请求必须带 ID，服务器要验证调用者有权访问它。
- **原则：** API 不该索要无法信任的东西，永远不要不经验证地信任请求体。
