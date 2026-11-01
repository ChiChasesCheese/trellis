---
id: hi-sd-api-gateway-1-why-gateway
node: qb.sd.distributed-rate-limiter.pre-sd-deep-dives-api-gateway
type: qa
step: 1
---
## Q
**API 网关为什么存在、第一职责是什么**｜系统设计 · 深入技术

微服务架构里 API 网关（API Gateway）解决什么问题？它的核心职责和附带职责分别是什么？

## A
**要点。** 网关是所有客户端请求的统一入口，让客户端不必知道内部有哪些服务、各在哪里，把内部拓扑和对外接口隔开。没有它，客户端要直接对接多个服务，耦合重、客户端代码复杂。

**核心职责。** 请求路由（request routing）：判断每个请求该交给哪个后端服务。

**附带职责。** 横切关注点（cross-cutting concerns）：鉴权、限流、缓存、SSL 终止等中间件。

**易错。** 很多人引入网关时只大谈中间件，却不说最根本的理由是路由。网关本身是瘦而简单的组件，不是系统的重点。
