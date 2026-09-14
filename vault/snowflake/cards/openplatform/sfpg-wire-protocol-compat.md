---
id: sfpg-wire-protocol-compat
node: openplatform.snowflake-postgres
type: qa
tags: [grown]
---
## Q
Snowflake Postgres 强调“协议兼容（wire-protocol compatible）”。这对已有应用和工具意味着什么？

## A
协议兼容指客户端与数据库之间使用标准的 Postgres 网络协议，因此现有的 Postgres 驱动（如 JDBC、psycopg）、ORM、迁移工具和 `psql` 可以直接连接，应用只需改连接串，而不必改用 Snowflake 专用驱动或重写 SQL。与之相对，把 OLTP 应用迁到一个“类 SQL”但方言和事务行为不同的系统，往往需要大量改写和回归测试。
