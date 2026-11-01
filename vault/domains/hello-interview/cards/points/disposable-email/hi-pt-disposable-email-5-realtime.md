---
id: hi-pt-disposable-email-5-realtime
node: qb.sd.disposable-email.points
type: qa
step: 5
---
## Q
**临时邮箱服务 · 实时展示新邮件**｜出自：临时邮箱服务 › 整体设计

新邮件要几秒内出现在网页上。后端和前端怎么配合？

## A
**要点。** 邮件写入后向 Redis 频道 `mbx:{address}` 发布事件；浏览器建立 SSE 连接，Web API 订阅该频道，收到事件就推新邮件摘要。
**兜底。** SSE 断开时前端每 5～10 秒轮询一次。
