---
id: grants-direct-to-user-ubac
node: security.rbac-ownership-and-grants
type: qa
source: snowflake-docs
---
## Q
Snowflake 除了把权限授予角色，也支持 `GRANT ... TO USER` 直接授予用户（UBAC，基于用户的访问控制）。直接授予用户的权限在什么条件下才会生效？

## A
只有当会话把次要角色设为全部（`USE SECONDARY ROLES ALL`）时，访问控制才会考虑直接授予用户的权限。常规做法仍是 RBAC：权限授予角色、角色授予用户，这样权限随角色集中管理；UBAC 是在此之上的补充，用于少数需要给个别用户单独授权的情况。
