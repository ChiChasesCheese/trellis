---
id: hi-sd-networking-essentials-4-sse-ws-webrtc
node: qb.sd.messenger-chat-system.pre-sd-core-concepts-networking-essentials
type: qa
step: 4
---
## Q
**SSE、WebSocket、WebRTC**｜系统设计 · 核心概念

需要服务端向客户端实时推送时，SSE、WebSocket、WebRTC 分别是什么机制？各自的适用场景和代价是什么？

## A
**要点。**
- SSE（Server-Sent Events）：在一个 HTTP 响应里分块持续推送，单向（服务端到客户端）。断线后 EventSource 带着最后收到的消息 ID 自动重连，服务端要负责补发漏掉的消息。
- WebSocket：先发 HTTP 升级握手，再接管同一条 TCP 连接，全双工、浏览器广泛支持，但具体消息格式要自己定义（常用 JSON）。
- WebRTC：浏览器之间点对点，底层用 UDP。需要信令服务器交换地址，用 STUN 打洞获得公网地址，失败时用 TURN 中继兜底。

**取舍。** 只需服务端推送就选 SSE，如拍卖的当前价格；真正需要高频双向再用 WebSocket；WebRTC 只留给音视频通话。

**易错。** 没有理由就上 WebSocket 会被扣分：有状态长连接贵，且途中的防火墙、代理、负载均衡都要支持。部分网络还会把 SSE 合并成一次响应。
