---
id: replication-edition-matrix
node: continuity.replication-and-failover
type: qa
source: snowflake-docs
---
## Q
一个标准版（Standard Edition）账户想把数据库、用户、角色和仓库都复制到另一个区域做灾备，能做到哪些？

## A
只能复制数据库和共享（share），并使用复制组，这些在所有版本都可用。复制用户、仓库、网络策略、集成等数据库和共享之外的账户级对象，以及使用故障转移组，都需要业务关键版（Business Critical Edition）或更高。因此标准版只能在目标区域得到只读的数据副本，无法完成账户级的故障转移。
