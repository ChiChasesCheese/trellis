---
id: rbac-role-owner-no-inherit
node: security.rbac-role-hierarchy
type: qa
source: snowflake-docs
---
## Q
角色 R_ADMIN 拥有（OWNERSHIP）角色 R_READ，那么 R_ADMIN 能不能直接使用 R_READ 上被授予的 SELECT 权限？Snowflake 里有没有能绕过授权检查的超级用户？

## A
不能。拥有一个角色只意味着可以管理这个角色（改属性、授予它），并不继承它的权限；权限继承只发生在角色层级中，即必须 `GRANT ROLE R_READ TO ROLE R_ADMIN` 才会继承。Snowflake 也没有任何可绕过授权检查的超级用户或超级角色，包括 ACCOUNTADMIN 在内，所有访问都需要相应的权限授予。
