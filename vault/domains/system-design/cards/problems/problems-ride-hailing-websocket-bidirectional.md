---
id: problems-ride-hailing-websocket-bidirectional
node: problems.geo.ride-hailing
type: qa
step: 3
tags: [grown]
---
## Q
In a ride-hailing app, why does the design choose WebSockets over Server-Sent Events (SSE) for real-time trip updates, given that SSE would be sufficient for a rider passively watching a driver's location move on a map?

## A
SSE is one-directional (server to client), which covers the rider's passive view fine, but the driver side needs to send data back over the same real-time channel — responding to match invitations and streaming frequent location updates — so SSE alone would force the driver client into two separate channels (SSE for receiving plus ordinary HTTP requests for sending). Choosing WebSockets, which are bidirectional, lets both the rider and driver clients use one connection protocol and lets the real-time delivery service implement a single connection-management path instead of two different ones for the two client types; the tradeoff is that WebSocket connections are stateful, so scaling the delivery service requires consistent-hash routing by connection, and reconnects need an explicit way to resend updates missed while disconnected.

## Q zh
在一个网约车 App 中，既然 Server-Sent Events（SSE）已经足够让乘客被动地在地图上看司机位置移动，为什么这个设计在实时行程更新上选择 WebSocket 而不是 SSE？

## A zh
SSE 是单向的（服务端到客户端），完全能覆盖乘客被动查看这一面，但司机端需要通过同一条实时通道把数据发回去——响应撮合邀请、持续上报高频位置更新——所以单用 SSE 会迫使司机端客户端拆成两条通道（SSE 收 + 普通 HTTP 请求发）。选择双向的 WebSocket，能让乘客端和司机端用同一种连接协议，也让实时推送服务只需要实现一套连接管理逻辑，而不是为两种客户端类型分别维护两套；代价是 WebSocket 连接本身是有状态的，推送服务的扩容需要按连接做一致性哈希路由，断线重连还需要一个明确的机制来补发断线期间错过的更新。
