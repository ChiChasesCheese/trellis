---
id: replication-group-vs-failover-group
node: continuity.replication-and-failover
type: qa
source: snowflake-docs
---
## Q
Snowflake 的复制组（replication group）和故障转移组（failover group）有什么区别？什么时候必须用后者？

## A
两者都是把源账户中一组对象作为一个单元复制到目标账户，并为目标账户上的对象提供时间点一致性（point-in-time consistency）。复制组在目标账户只提供只读副本；故障转移组是还能「故障转移」的复制组：其中任一被允许的目标账户可以把自己的次级组提升（promote）为主组，从而获得读写权限。需要在灾难时把业务切到另一区域或另一云继续写入，就必须用故障转移组，而它要求业务关键版（Business Critical Edition）或更高。
