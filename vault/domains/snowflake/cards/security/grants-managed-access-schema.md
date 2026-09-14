---
id: grants-managed-access-schema
node: security.rbac-ownership-and-grants
type: qa
source: snowflake-docs
---
## Q
一个团队里每个人都能建表，结果各自把表的 SELECT 随手授予给别人，权限失控。托管访问模式（managed access schema）怎样解决这个问题？

## A
在托管访问模式中，对象所有者失去授权决定权：只有模式的所有者（持有该 schema 的 OWNERSHIP 的角色）或持有 MANAGE GRANTS 权限的角色才能给模式内的对象授予权限，包括 future grant。这样建表的人仍然拥有表，但“谁能访问”集中由模式所有者或安全管理员决定，实现集中式权限管理。
