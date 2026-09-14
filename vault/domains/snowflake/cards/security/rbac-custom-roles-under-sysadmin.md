---
id: rbac-custom-roles-under-sysadmin
node: security.rbac-role-hierarchy
type: qa
source: snowflake-docs
---
## Q
新建一套自定义角色（custom role）来拥有数据库对象时，为什么推荐把这套层级的最顶端角色授予给系统角色 SYSADMIN？如果不这样做会怎样？

## A
挂到 SYSADMIN 下后，SYSADMIN 通过继承获得这些自定义角色的所有权限，系统管理员就能统一管理账户里的仓库和数据库对象，而用户与角色的管理仍由 USERADMIN 负责，职责分离。如果不挂上去，SYSADMIN 无法管理这些角色拥有的对象，只有具备 MANAGE GRANTS 权限的角色（默认只有 SECURITYADMIN）能看到这些对象并修改其授权，形成管理盲区。
