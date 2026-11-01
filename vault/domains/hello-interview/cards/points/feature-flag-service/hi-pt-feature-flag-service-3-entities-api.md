---
id: hi-pt-feature-flag-service-3-entities-api
node: qb.sd.feature-flag-service.points
type: qa
step: 3
---
## Q
**功能开关服务 · 实体与双平面接口**｜出自：功能开关服务 › 核心实体与接口

功能开关服务的核心实体有哪些？控制面和数据面的接口各是什么？为什么控制面修改要带期望版本号？

## A
**实体。** Flag（key、变体、默认变体）、FlagConfig（某环境的有序规则列表、是否启用、单调递增 version）、Rule（条件加动作）、Segment（人群）、AuditEvent。
**控制面。** `PUT /flags/{key}/environments/{env}` 带期望版本号做乐观并发控制，`rollback?to=version`。
**数据面。** `GET /sdk/config` 返回整份快照（带 ETag）；`GET /sdk/stream` 用 SSE 推变更；客户端用 `POST /eval`。
