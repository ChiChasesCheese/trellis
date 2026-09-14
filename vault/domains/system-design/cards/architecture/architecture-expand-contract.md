---
id: architecture-expand-contract
node: architecture.discovery
type: qa
---
## Q
You need a breaking API change (rename a field, change semantics) with consumers you don't control deploying on their own schedule. What's the migration pattern?

## A
**Expand and contract** (parallel change):
1. **Expand**: serve both old and new shapes (add the new field/endpoint/version alongside the old; dual-write or translate).
2. **Migrate**: consumers move at their own pace; you track usage of the old shape with metrics per consumer.
3. **Contract**: remove the old shape only when telemetry shows zero callers (then announce, then delete).

Guard the whole thing with **consumer-driven contract tests** (e.g. Pact): each consumer publishes the requests/fields it relies on, and the provider's CI fails before a deploy would break them — turning "did we break anyone?" from archaeology into a test failure.

## Q zh
你需要一个破坏 API 改变（重命名字段、改变语义）与控制之外的消费者自己的计划部署。什么是迁移模式？

## A zh
**扩展和契约**（并行改变）：
1. **扩展**：服务两个旧和新形状（添加新字段/端点/版本沿着旧；双写或翻译）。
2. **迁移**：消费者按他们自己的步速移动；你用每个消费者的指标跟踪旧形状的使用。
3. **契约**：仅当遥测显示零调用者时移除旧形状（然后公告，然后删除）。

用**消费者驱动契约测试**保护整个事物（例如 Pact）：每个消费者发布它依赖的请求/字段，提供者的 CI 在部署会打破他们之前失败——将"我们打破任何人吗？"从考古变成测试失败。
