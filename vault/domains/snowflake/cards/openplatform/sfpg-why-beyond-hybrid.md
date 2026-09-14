---
id: sfpg-why-beyond-hybrid
node: openplatform.snowflake-postgres
type: qa
tags: [grown]
---
## Q
Snowflake 已经有面向 OLTP 的混合表（hybrid table），为什么还要在平台内提供托管的 Snowflake Postgres？什么样的应用更适合后者？

## A
混合表是 Snowflake SQL 引擎里的一种表类型，只提供行存、强制主键/外键、行锁等有限的事务能力，SQL 方言和功能也是 Snowflake 的。Snowflake Postgres 是真正的 Postgres 实例，提供完整的 Postgres 事务语义、SQL 方言、扩展（extension）生态和线协议兼容。已经基于 Postgres 开发、依赖其特有功能（如触发器、特定扩展、存储过程语言）或 ORM 行为的现有应用，可以不改代码迁入；只需少量低延迟点读写并与分析数据紧密结合的新负载，混合表往往更简单。
