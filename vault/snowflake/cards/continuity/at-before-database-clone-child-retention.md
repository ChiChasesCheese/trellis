---
id: at-before-database-clone-child-retention
node: continuity.at-before-statement-syntax
type: qa
source: snowflake-docs
---
## Q
数据库 `db1` 保留期 7 天，其中表 `t1` 保留期 1 天。执行 `CREATE DATABASE db2 CLONE db1 AT(OFFSET => -2*86400)`（两天前）会发生什么？怎么绕过？

## A
克隆失败：指定的时间点超出了当前子对象 `t1` 的保留期，`t1` 两天前的历史数据已不在时间旅行（Time Travel）中。可以加上 `IGNORE TABLES WITH INSUFFICIENT DATA RETENTION`，跳过历史数据不足的表，克隆其余对象。另外，如果指定时间点早于或等于对象的创建时间，克隆同样会失败。
