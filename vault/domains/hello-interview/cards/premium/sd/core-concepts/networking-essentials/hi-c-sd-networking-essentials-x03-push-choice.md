---
id: hi-c-sd-networking-essentials-x03-push-choice
node: sd.core-concepts.networking-essentials.exam
type: qa
step: 3
---
## Q
**网络基础 · 实时推送的方案**｜考点 · 必会

拍卖要把当前最高价实时推给竞拍者。轮询、SSE、WebSocket 怎么选？

## A
- **SSE 合适：** 只需服务器单向推送，建立在 HTTP 之上，断线后 `EventSource` 自动带最后的消息 ID 重连，服务器补发漏掉的消息。
- **WebSocket 过度：** 不需要高频双向通信，有状态长连接的基础设施贵，还要所有中间设施都支持。没有理由上 WebSocket 会被扣分。
- **轮询：** 最简单，但有延迟和空请求负载，更新不频繁时可用。
- **说出 SSE 的局限：** 连接会被服务器、均衡器或代理关闭，有的网络会把 SSE 响应攒成一次；这说明你真的用过。
- **配套：** 长连接服务选最少连接的负载均衡。
