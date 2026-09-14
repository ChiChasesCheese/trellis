---
id: clone-ddl-rename-conflict
node: continuity.zero-copy-clone
type: qa
source: snowflake-docs
---
## Q
克隆数据库的过程中，另一个会话删除了表 `t_sales`，并把另一张表改名为 `t_sales`，克隆随即报错。为什么克隆会被这种 DDL 干扰？

## A
克隆很快但不是瞬时的，而 DDL 是原子的、不属于多语句事务，克隆期间对源对象执行的 DDL 可能不会反映在克隆中。Snowflake 也不记录克隆开始时有哪些对象名、之后哪些名字变过，因此重命名或删除后重建子对象会与进行中的克隆争用名字，导致名字冲突。建议克隆完成前不要把对象改名为某个已删除对象用过的名字。
