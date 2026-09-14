---
id: traffic-gateway-centralizes
node: traffic.gateways
type: qa
---
## Q
An API gateway sits in front of 30 microservices. Which cross-cutting concerns does it centralize that would otherwise be reimplemented 30 times?

## A
- **TLS termination** — one place holding certs.
- **Authentication** — validate the JWT/session once, forward trusted identity headers; services skip auth logic.
- **Routing & versioning** — path → service mapping, canary splits.
- **Protection** — rate limits, quotas, request size caps, WAF.

Plus observability chokepoint: uniform access logs, metrics, and trace-id injection for every request entering the system.

## Q zh
API 网关坐在 30 个微服务的前面。它集中化哪些横切关切，否则会重新实现 30 次？

## A zh
- **TLS 终止** — 一个地方持有证书。
- **身份验证** — 验证 JWT/会话一次，转发受信身份头；服务跳过身份验证逻辑。
- **路由和版本化** — 路径 → 服务映射、金丝雀分流。
- **保护** — 速率限制、配额、请求大小上限、WAF。

加上可观测性瓶颈：统一访问日志、指标和每个进入系统的请求的 trace-id 注入。
