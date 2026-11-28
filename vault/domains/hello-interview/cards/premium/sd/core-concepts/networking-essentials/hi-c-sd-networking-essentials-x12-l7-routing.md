---
id: hi-c-sd-networking-essentials-x12-l7-routing
node: sd.core-concepts.networking-essentials.exam
type: qa
step: 12
---
## Q
**网络基础 · 一个入口按路径路由**｜考点 · 必会

想让 `/api/*` 走一组服务器、`/static/*` 走另一组，并让同一用户落在同一台上。用什么？

## A
- **L7 负载均衡：** 终止连接，读取 URL、头部和 Cookie 做路由，功能类似 API 网关。
- **会话保持：** 基于 Cookie（或 IP 哈希算法）让同一用户落在同一台服务器。
- **代价：** 比 L4 更耗 CPU，因为要检查内容。
- **反例：** L4 看不到 URL，只能按 IP 和端口转发，做不了路径路由。
- **提醒：** 会话保持会让服务器有状态，能做成无状态就不要依赖它。
