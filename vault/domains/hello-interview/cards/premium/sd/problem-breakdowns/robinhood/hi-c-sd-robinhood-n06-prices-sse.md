---
id: hi-c-sd-robinhood-n06-prices-sse
node: sd.problem-breakdowns.robinhood.notes
type: qa
step: 6
---
## Q
**股票交易平台 · 实时行情：SSE 推送**｜摘要 · 必会

为什么行情推送选 SSE 而不是 WebSocket？接入 SSE 之后接口怎么变，又带来什么新问题？

## A
- **SSE（Server-Sent Events）：** 基于 HTTP 的持久连接，单向，服务端向客户端推。行情只需服务端推、客户端不发数据，所以比双向的 WebSocket 更合适：协议更简单，走普通 HTTP，自动重连。
- **接口改动：** 变成 `GET /subscribe?symbols=A,B`。后端在客户端与符号服务之间建立 SSE 连接，先发一次初始价格列表，由缓存提供，缓存由监听交易所的处理器保持最新；处理器同时把后续价格推给符号服务，再转发给订阅这些符号的客户端。
- **新问题：**
  - 负载均衡要支持粘性会话（sticky session），连接才能一直落在同一台服务器；
  - 持久连接意味着要考虑断线和重连：重连后怎么补齐错过的价格；
  - 怎么把某个符号的价格路由到正好连着关心它的用户的那些服务器上（做法见 Redis 发布订阅路由行情一节）。
- **模式。** 实时更新（real-time updates）：长连接推送代替轮询，面对只读的广播型数据首选 SSE。
