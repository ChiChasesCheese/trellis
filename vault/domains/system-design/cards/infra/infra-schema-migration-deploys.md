---
id: infra-schema-migration-deploys
node: infra.delivery
type: qa
---
## Q
Why are database schema changes the riskiest class of deploy, and how does expand–contract make them safe?

## A
Two reasons: during any rolling or canary deploy, **old and new code run against the same schema simultaneously**; and destructive migrations (drop, rename, type change) **cannot be rolled back** — the data is gone.

Expand–contract at the schema level:
1. **Expand**: additive-only change (new nullable column / new table) that old code safely ignores.
2. **Migrate**: ship code that dual-writes, backfill old rows asynchronously, then switch reads to the new shape.
3. **Contract**: drop the old column in a *later* deploy, only after telemetry shows nothing reads it.

Rule: every migration must be compatible with the code version before *and* after it — never couple a destructive migration to the code deploy that wants it.

## Q zh
为什么数据库 schema 改变是最危险的部署类别，expand-contract 如何使它们安全？

## A zh
两个原因：在任何滚动或 canary 部署期间，**旧和新代码针对相同 schema 同时运行**；和破坏性迁移（drop、rename、type 改变）**不能被回滚**——数据消失了。

在 schema 级别 Expand-contract：
1. **Expand**：仅加性改变（新可空列/新表），旧代码安全地忽略。
2. **Migrate**：发货双写的代码，异步 backfill 旧行，然后切换读到新形状。
3. **Contract**：在**后来的**部署中 drop 旧列，仅在遥测显示什么都不读它之后。

规则：每个迁移必须与**之前和之后**的代码版本兼容——永不将破坏性迁移耦合到想要它的代码部署。
