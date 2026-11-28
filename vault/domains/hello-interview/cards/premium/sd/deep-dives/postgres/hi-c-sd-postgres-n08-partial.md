---
id: hi-c-sd-postgres-n08-partial
node: sd.deep-dives.postgres.notes
type: qa
step: 8
---
## Q
**PostgreSQL · 部分索引**｜摘要 · 必会

只需要索引一部分行时怎么办？

## A
- **部分索引（partial index）：** 在建索引时加 `WHERE` 条件，只索引满足条件的行，例如 `ON users(email) WHERE status = 'active'`。
- **适用情形：** 绝大多数查询只关心一个子集（活跃用户）；表里有大量不需要查的行（已删除、已归档）；想减少索引大小和维护开销。
- **好处：** 索引更小更快，更新这些"冷"行时无需更新索引。
- **限制：** 查询的条件必须蕴含索引的条件，否则优化器用不了它，所以查询里要带上同样的过滤。
