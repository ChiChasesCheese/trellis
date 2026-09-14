---
id: retention-dropped-container-overrides-child
node: continuity.retention-vs-failsafe
type: qa
source: snowflake-docs
---
## Q
数据库 `db` 的保留期是 1 天，其中表 `t` 显式设为 30 天。如果直接 DROP 整个数据库，`t` 能在第 10 天被恢复吗？如何避免？

## A
不能。删除数据库时，子模式或子表上显式设置的、与数据库不同的保留期不会被遵守，子对象跟随数据库的保留期（1 天）一起过期；删除模式时对子表也是如此。若要让子对象按自己的保留期保留，应先显式 DROP 这些子对象，再删除数据库或模式。
