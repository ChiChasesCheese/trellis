---
id: traffic-reverse-proxy-vs-gateway
node: traffic.gateways
type: qa
---
## Q
Reverse proxy vs API gateway — same box or different? Draw the line.

## A
Same mechanical position (server-side intermediary terminating client requests), different altitude:

- **Reverse proxy** (nginx, Envoy) is the *mechanism*: forwarding, TLS, buffering, compression, caching, basic routing.
- **API gateway** is a reverse proxy plus **API-level policy**: per-client auth, quotas/billing, version routing, request/response transformation, developer-facing API management.

In practice gateways are built *on* reverse proxies. If you only need "route and terminate TLS," a plain reverse proxy is less machinery to operate.

## Q zh
反向代理 vs API 网关 — 相同的框或不同？画出线。

## A zh
相同的机械位置（服务器侧中介终止客户端请求），不同的高度：

- **反向代理**（nginx、Envoy）是*机制*：转发、TLS、缓冲、压缩、缓存、基本路由。
- **API 网关**是反向代理加上**API 级策略**：每客户端身份验证、配额/计费、版本路由、请求/响应转换、面向开发者的 API 管理。

实际上网关构建*在*反向代理上。如果你只需要"路由和终止 TLS，"普通反向代理是较少的操作机制。
