---
id: hi-ov-chatgpt-3-when
node: sd.problem-breakdowns.chatgpt
type: qa
step: 3
tags: [通览]
---
## Q
**ChatGPT · 深挖清单**｜通览

ChatGPT 会被追问哪些深挖？各自的做法和代价是什么？

## A
- **流式输出：** SSE（HTTP 上服务器持续推送），POST 返回 runId 后 GET 订阅；轮询拖慢首 token，WebSocket 太重；客户端要说的话（如停止）得另发请求。
- **断线续传：** Redis Stream 日志，按 ID 续读（pub/sub 是另一选项）；pub/sub 换实例的空窗会永久丢 token；Stream 不是记录，完整消息仍写 Postgres。
- **GPU 调度：** 请求入队，工作者拉取，连续批处理（一块 GPU 同时推进几十条生成），队列限深；吸收尖峰、让 GPU 保持忙；服务层更复杂。
- **公平分配：** 按用户的 token 令牌桶，入场预留最大输出、结束退还，付费层优先；每用户限流只数请求不数成本；预留按最坏情况，免费层要留保底。
- **上下文成本：** 滚动摘要加前缀缓存（复用已算过的前文），截断便宜但会失忆；50 轮后每轮要发约 2.5 万输入 token；摘要多调一次模型，每轮重写会让缓存失效。
- **取消一次生成：** 显式 POST 取消，工作者收到信号停止；回收 GPU；关页不等于取消。

**各级别。** 中级想到 SSE 与队列；高级至少深入两项；Staff 算 GPU 账、自己想到前缀缓存。
