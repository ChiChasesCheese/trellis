---
id: grants-ownership-dac
node: security.rbac-ownership-and-grants
type: qa
source: snowflake-docs
---
## Q
在 Snowflake 中，“拥有”一个对象意味着什么？对象默认归谁所有，所有者在普通模式（schema）里能做什么？

## A
拥有对象就是某个角色持有该对象的 OWNERSHIP 权限。每个可授权对象（securable object）恰好只有一个所有者角色，默认是创建它时的当前主角色。在普通模式里，所有者角色默认拥有该对象的全部权限，并且可以把权限 GRANT/REVOKE 给其他角色，这就是自主访问控制（DAC，Discretionary Access Control）。所有权可以用 `GRANT OWNERSHIP` 转移给另一个角色（包括数据库角色）；被授予该所有者角色的所有用户实际上共同控制这个对象。
