---
id: rbac-secondary-roles-create-rule
node: security.rbac-role-hierarchy
type: qa
source: snowflake-docs
---
## Q
用户会话里主角色（primary role）是 ANALYST，又用 `USE SECONDARY ROLES ALL` 激活了次要角色（secondary roles）。执行 CREATE TABLE 和执行跨库 JOIN 查询时，分别由哪些角色的权限来授权？

## A
CREATE 语句只由主角色（及其继承的下层角色）授权，新建对象的所有权也归当前主角色，这样对象的归属是确定的。除 CREATE 之外的其他操作（如 SELECT、跨库 JOIN、对已拥有对象做 DDL）可以使用主角色和所有次要角色及其继承角色权限的并集。因此次要角色适合跨库查询这类场景，避免专门再建一个父角色把各库的角色合并起来。一个会话恰好有一个主角色，但可以同时激活任意多个次要角色。
