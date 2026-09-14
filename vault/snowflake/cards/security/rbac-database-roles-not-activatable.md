---
id: rbac-database-roles-not-activatable
node: security.rbac-role-hierarchy
type: qa
source: snowflake-docs
---
## Q
数据库角色（database role，权限范围限定在单个数据库内的角色）和账户角色（account role）在角色层级里的使用规则有什么不同？用户怎样才能用上一个数据库角色的权限？

## A
数据库角色不能在会话中直接激活，既不能作主角色也不能作次要角色；要使用它的权限，必须把它授予给一个账户角色，再激活该账户角色。方向上也有限制：账户角色不能被授予给数据库角色。这样数据库角色始终是挂在账户角色之下的“权限包”，便于把某个库的权限整体授予或随共享（share）一起交出。
