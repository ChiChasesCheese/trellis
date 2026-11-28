---
id: hi-c-sd-chatgpt-n06-streaming
node: sd.problem-breakdowns.chatgpt.notes
type: qa
step: 6
---
## Q
**ChatGPT · 深入一：把 token 流式送到浏览器**｜摘要 · 必会

怎样把模型生成的 token 实时显示给用户？轮询、WebSocket、SSE 各有什么优缺点，工作者到聊天服务那一跳用什么？

## A
- **内部一跳：** 工作者到聊天服务用 gRPC 服务端流（HTTP/2 上的一次调用，工作者沿着打开的连接逐个 token 发回）。普通请求响应会迫使工作者攒完 30 秒的回答再一次给出，又变回空白屏。内部服务之间选 gRPC 是因为 HTTP/2 二进制帧与多路复用，加 protobuf 的强类型契约。
- **轮询（差）：** 客户端每几百毫秒问一次，token 要先放在某个缓冲里。首 token 被轮询间隔拖慢，12 万路每 300 ms 一次约 40 万请求/秒且大多为空，回答成批出现而非逐字。
- **WebSocket（可用）：** 常驻双向连接，服务器随时推送，首 token 只受模型限制。但生成期间只有单向推送，却要背负升级握手、有状态连接，且路径上每个负载均衡与代理都要支持。
- **SSE（最合适）：** 浏览器用 `EventSource` 发普通 HTTP 请求，服务器保持响应打开并持续写 `data:` 事件。纯 HTTP、无协议升级，所有代理已支持；浏览器会自动重连；后端不变，聊天服务仍从 gRPC 收 token 再转发。
