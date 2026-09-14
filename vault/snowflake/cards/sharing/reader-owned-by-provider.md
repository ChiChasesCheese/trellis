---
id: reader-owned-by-provider
node: sharing.reader-accounts
type: qa
source: snowflake-docs
---
## Q
只读账户（reader account）和普通完整账户作为数据消费方时，在“能从谁那里消费数据”上有什么根本区别？

## A
每个只读账户都隶属于创建它的提供方账户，并且只能消费该提供方共享的数据，不能导入其他提供方的 share。完整账户则可以同时消费任意多个提供方的 share，自己也能作为提供方创建 share。
