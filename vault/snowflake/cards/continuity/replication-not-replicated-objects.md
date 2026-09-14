---
id: replication-not-replicated-objects
node: continuity.replication-and-failover
type: qa
source: snowflake-docs
---
## Q
故障转移之后，团队发现目标账户里少了一些表和对象。数据库复制时哪些常见对象不会被复制？这对灾备演练有什么启示？

## A
不支持复制的对象在复制时会被直接跳过，故障转移后在目标账户中也不存在。常见的有：临时表（temporary table）、外部表（external table）、混合表（hybrid table）、事件表（event table）和临时暂存区；暂存区（stage）和管道（pipe）只能通过复制组或故障转移组复制，单纯的数据库复制不包含它们。灾备演练时应按不被复制的对象清单逐一核对，不能假设整个数据库原样可用。
