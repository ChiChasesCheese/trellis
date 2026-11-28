---
id: hi-c-sd-chatgpt-x04-resume-point
node: sd.problem-breakdowns.chatgpt.exam
type: qa
step: 4
---
## Q
**ChatGPT · 故障：发布期间丢了多少 token，续传从哪里开始**｜考点 · 必会

聊天服务滚动发布，某路流的旧实例掉线、新实例 2 秒后才连上。假设模型每秒产出 40 个 token。用 pub/sub 和用 Redis Stream 各是什么结果？Stream 方案里新实例怎么知道从哪读？

## A
- **pub/sub：** 空窗 2 秒，工作者仍在发布，没有订阅者，约 80 个 token（40×2）永久丢失，回答中间有洞，要等生成完毕、客户端重新拉整条消息才补上。
- **Stream：** 这 80 个条目都写在日志里，新实例从客户端最后见到的 ID 继续 `XREAD`，补齐后再接实时读，用户看到连续回答。
- **怎么知道 ID：** 每个 SSE 事件带一个 `id:` 字段，值就是 Stream 条目 ID；浏览器 `EventSource` 重连时自动在请求头里带 `Last-Event-ID`，新实例据此从该 ID 之后读。
- **边界：** 超过 `MAXLEN` 窗口或 TTL 之后，旧条目已被回收，此时无法续传，就只能让客户端从 Postgres 取最终消息。窗口要大于最长预期的断线时间。
