---
id: hi-sd-distributed-rate-limiter-2-entities-identify
node: sd.problem-breakdowns.distributed-rate-limiter.exam
type: qa
step: 2
---
## Q
**核心实体、接口与客户端识别**｜系统设计 · 问题拆解

限流器有哪些核心实体和接口？用什么标识一个客户端，多条规则同时适用时怎么判断？

## A
**实体。** 规则（Rules：时间窗口内次数、适用的客户端和端点）、客户端（Clients：用户 / IP / API key 及其用量状态）、请求（Requests：身份、端点、时间戳）。

**接口。** `isRequestAllowed(clientId, ruleId) -> { passes, remaining, resetTime }`，后两个字段用于响应头。

**识别方式。**
- 用户 ID：已登录 API，通常来自 Authorization 里的 JWT
- IP：公开 API，但注意 NAT、公司防火墙后的多用户；来自 X-Forwarded-For
- API key：开发者 API，在 X-API-Key 头

**组合规则。** 现实里分层叠加：每用户、每 IP、全局、特定端点各有限额。检查所有适用规则，执行最严格的那条；Alice 用了 1000 次里的 50，但她的 IP 已超 100 次，也要拦截。
