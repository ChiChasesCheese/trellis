---
id: networking-grpc-streaming-modes
node: networking.api-styles
type: qa
---
## Q
gRPC's four call types — match each to its use, and name the operational caveat long-lived streams create.

## A
- **Unary**: ordinary request/response — the default.
- **Server-streaming**: subscriptions and feeds — replaces client polling with pushed increments.
- **Client-streaming**: uploads and telemetry — batch many messages into one call, single response.
- **Bidirectional**: chat, sync protocols, interactive sessions.

Caveat: a stream lives on one HTTP/2 connection, so it **pins to one backend** for its lifetime — draining and rebalancing need max-connection-age or app-level reconnects ([[traffic-http2-connection-pinning]]).

## Q zh
gRPC 的四种调用类型 — 将各自匹配到其用途，并命名长连接流创建的运维警告。

## A zh
- **一元**：普通请求/响应 — 默认。
- **服务器流**：订阅和源 — 用推送增量替代客户端轮询。
- **客户端流**：上传和遥测 — 将许多消息批处理为一个调用、单一响应。
- **双向**：聊天、同步协议、交互式会话。

警告：一个流生存在一个 HTTP/2 连接上，所以它**在其生命周期内固定在一个后端** — 排空和重新平衡需要 max-connection-age 或应用级重连接（[[traffic-http2-connection-pinning]]）。
