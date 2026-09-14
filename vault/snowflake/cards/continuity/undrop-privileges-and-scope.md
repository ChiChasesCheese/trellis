---
id: undrop-privileges-and-scope
node: continuity.undrop-recovery
type: qa
source: snowflake-docs
---
## Q
一个只有某张表 SELECT 权限的分析师，能用 UNDROP 恢复这张被误删的表吗？恢复还有什么位置上的限制？

## A
不能。与删除对象一样，恢复需要该对象的 OWNERSHIP（所有权）权限，另外还需要在目标数据库或模式上拥有创建该类对象的 CREATE 权限。并且表和模式只能在当前模式或当前数据库中恢复，即便写了完全限定名也是如此。
