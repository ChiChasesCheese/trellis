---
id: undrop-retention-zero-and-alter-dropped
node: continuity.undrop-recovery
type: qa
source: snowflake-docs
---
## Q
模式 `s1` 保留期 90 天，其中表 `t1` 被删除后，把 `s1` 的保留期改成 1 天，`t1` 的可恢复期限会变吗？如果表的保留期本来就是 0，删除后还能恢复吗？

## A
`t1` 的可恢复期限不变，仍按 90 天保留：修改数据库或模式的保留期只影响其中仍活跃的对象，已删除的对象不受影响；要改变已删除对象的保留期，必须先 UNDROP 再 ALTER。保留期为 0 的对象被删除后无法恢复，这就是一般建议每个对象至少保留 1 天的原因。
