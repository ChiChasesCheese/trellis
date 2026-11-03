---
id: hi-pt-feature-flags-service-2-flag-entity
node: qb.sd.feature-flags-service.points
type: qa
step: 2
---
## Q
**功能开关服务 · 开关实体与接口**｜必会 · 出自：功能开关服务 › 核心实体与接口

`Flag` 实体要有哪些字段？控制面和数据面各暴露什么接口？浏览器、手机为什么不拿规则快照？

## A
**实体。** `Flag(key, enabled, variants, rolloutPercent, rules, salt, version…)` 加评估上下文 `Context`、`AuditLog`。
**接口。** 控制面 `PUT /flags/{key}`（带版本）、`rollback`；SDK `isEnabled`、`variant`。
**客户端。** 不下发规则（泄露策略且太大），请求边缘评估服务 `GET /evaluate` 取已解析的值。
