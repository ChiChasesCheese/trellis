---
id: replication-graceful-failover-suspend-schedule
node: continuity.replication-and-failover
type: qa
source: snowflake-docs
---
## Q
在目标账户执行计划内的故障转移（把次级故障转移组提升为主组）时，为什么应先暂停定时复制？

## A
刷新（refresh）正在执行时，次级故障转移组不能被提升为主组。为了平滑地完成故障转移，应先在目标账户暂停调度的复制，确保没有刷新在跑，再执行提升；故障转移完成后再恢复定时复制。
