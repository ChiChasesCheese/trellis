---
id: hi-c-sd-chatgpt-n08-resume-stream
node: sd.problem-breakdowns.chatgpt.notes
type: qa
step: 8
---
## Q
**ChatGPT · 深入二：怎样让流在重连和发布时不断**｜摘要 · 必会

聊天服务实例随时会重启，怎么保证用户的流不丢 token？pub/sub 与 Redis Stream 各自的结果是什么？

## A
- **问题：** 持有 SSE 连接的实例同时持有 gRPC 流，必须全程不倒；但聊天层无状态、横向扩展、一天发布多次，实例消失是常态。要把"产生 token 的工作者"和"投递 token 的实例"解耦。
- **Redis pub/sub（好但有洞）：** 按 runId 建频道，工作者发布，持有连接的实例订阅转发，重连的新实例订阅同一频道即可。要发**增量（delta）**而不是累计全文：累计全文是平方级，4000 个 token 的回答会把一个越来越长的前缀重发 4000 次。缺点：发射即忘，旧实例掉线、新实例尚未订阅的空窗里，工作者继续发的 token 永久丢失，回答中间出现一个洞。
- **Redis Stream（更好）：** 每个 runId 一个只追加的日志，条目有 ID。工作者 `XADD` 增量，实例用阻塞的 `XREAD` 从客户端最后见到的 ID 读，重连后补齐缺的条目再接着实时读。用 `MAXLEN` 限长、短 TTL 回收，内存可控。
- **边界：** Stream 不是系统的记录，生成结束时工作者把完整助手消息写 Postgres 并将 Run 标为 done，那才是持久副本；Stream 只负责让实时流在重连时没有缺口，所以逐 token 持久化仍在线外。
