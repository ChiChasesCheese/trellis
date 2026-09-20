---
id: problems-live-comments-sse-vs-websocket
node: problems.social.live-comments
type: qa
step: 2
tags: [grown]
---
## Q
For broadcasting live comments to viewers of a live video, why is SSE (Server-Sent Events) generally preferred over WebSockets, given that viewers mostly read comments and only occasionally post one?

## A
The traffic is highly asymmetric — server-to-viewer (broadcasting comments) vastly outweighs viewer-to-server (posting a comment, which is rare per viewer). SSE only supports server-to-client push, which matches this shape exactly, and it comes with automatic reconnection and a `Last-Event-ID` header for resuming after a drop, all over plain HTTP that works through existing proxies and load balancers. WebSockets are genuinely bidirectional, but paying for that with a WebSocket fleet's operational complexity (connection registries, affinity routing, connection migration on deploy) isn't justified when the client-to-server direction is used so rarely; posting a comment can just be a separate, ordinary HTTP POST outside the broadcast channel.

## Q zh
在向一场直播的观众广播评论时，考虑到观众多数只读评论、偶尔才发一条，为什么通常优先选择 SSE（Server-Sent Events）而不是 WebSocket？

## A zh
流量高度不对称——服务器到观众（广播评论）远大于观众到服务器（发一条评论，每个观众很少发生）。SSE 只支持服务器到客户端的推送，正好匹配这个形状，并且自带自动重连和 `Last-Event-ID` 头用于断线后续传，全部走普通 HTTP，能直接利用现有代理和负载均衡。WebSocket 是真正双向的，但为此付出 WebSocket 舰队的运维复杂度（连接注册表、亲和路由、部署时连接迁移）在客户端到服务器方向用量如此稀疏时并不划算；发评论完全可以是广播通道之外一次独立的普通 HTTP POST。
