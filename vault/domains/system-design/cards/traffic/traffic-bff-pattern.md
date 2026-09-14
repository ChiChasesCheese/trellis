---
id: traffic-bff-pattern
node: traffic.gateways
type: qa
---
## Q
Backend-for-Frontend: what failure of the single shared API gateway does it address, and at what cost?

## A
A single gateway serving web, mobile, and partners accretes conflicting per-client logic — payload shaping, aggregation, feature quirks — owned by no one (the god-box problem, [[traffic-gateway-risks]]).

**BFF**: one thin edge service per client type, owned by that client's team — the mobile BFF aggregates and trims for constrained devices; the web BFF evolves independently.

Cost: more deployables and the temptation to duplicate cross-cutting policy — so auth, rate limiting, and TLS stay in a shared gateway layer *beneath* the BFFs; BFFs hold only per-client shaping.

## Q zh
后端即前端（Backend-for-Frontend）：它解决了单一共享 API 网关的什么故障，代价是什么？

## A zh
单一网关服务 web、mobile 和合作伙伴会累积矛盾的每客户端逻辑 — 负载塑形、聚合、功能怪癖 — 没人拥有（god-box 问题，[[traffic-gateway-risks]]）。

**BFF**：每个客户端类型一个瘦边缘服务，由该客户端的团队拥有 — mobile BFF 为受限设备聚合和修剪；web BFF 独立演进。

代价：更多可部署物和复制横切逻辑的诱惑 — 所以 auth、rate limiting 和 TLS 留在 BFF*下方*的共享网关层；BFF 只持有每客户端塑形。
