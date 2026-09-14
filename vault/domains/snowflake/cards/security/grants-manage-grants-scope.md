---
id: grants-manage-grants-scope
node: security.rbac-ownership-and-grants
type: qa
source: snowflake-docs
---
## Q
SECURITYADMIN 持有全局 MANAGE GRANTS 权限，它能否直接创建一个数据库角色或建表？MANAGE GRANTS 的边界在哪里？

## A
不能直接创建。MANAGE GRANTS 只提供授予和撤销权限的能力——它可以修改或撤销账户里的任意授权，即使自己不是对象所有者——但不包含创建对象等其他操作。要创建对象（如数据库角色），SECURITYADMIN 还必须被授予相应的创建权限（如 CREATE DATABASE ROLE）。不过持有 MANAGE GRANTS 的角色可以把额外权限授予给自己（授权者角色），所以它仍是高度敏感的权限。
