---
id: reader-why-exists
node: sharing.reader-accounts
type: qa
source: snowflake-docs
---
## Q
Snowflake 数据共享只能在 Snowflake 账户之间进行。如果合作方根本没有 Snowflake 账户、也不打算成为付费客户，提供方怎样把数据共享给它？

## A
提供方为其创建一个只读账户（reader account，旧称 read-only account）。它是一种快速、低成本的方式，让没有 Snowflake 账户的消费方无需成为 Snowflake 客户即可查询共享数据。提供方照常创建 share，再把 share 共享给这个只读账户。
