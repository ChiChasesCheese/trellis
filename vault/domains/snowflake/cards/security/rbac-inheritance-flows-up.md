---
id: rbac-inheritance-flows-up
node: security.rbac-role-hierarchy
type: qa
source: snowflake-docs
---
## Q
Snowflake 的 RBAC（基于角色的访问控制）中，Role 3（有权限 C）被授予给 Role 2（有权限 B），Role 2 被授予给 Role 1（有权限 A），Role 1 授予给 User 1。每个角色和 User 1 最终各有哪些权限？权限沿哪个方向流动？

## A
把一个角色授予给另一个角色，就形成角色层级（role hierarchy），下层角色的权限被其上所有角色继承，即权限向上流动：Role 2 有 B、C；Role 1 有 A、B、C；User 1 通过 Role 1 拥有全部三个权限。Role 3 自己仍只有 C，下层不会反向获得上层权限。由于一个角色可以被授予给多个角色，层级是有向无环图（DAG）而不是树。
