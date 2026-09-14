---
id: rap-policy-owner-evaluation
node: security.row-access-policies
type: qa
source: snowflake-docs
---
## Q
行级访问策略（row access policy）里引用了一张映射表（mapping table，如“销售经理 → 可见区域”），但普通查询用户对这张映射表没有 SELECT 权限。查询会失败吗？为什么？

## A
不会失败。Snowflake 以策略所有者（policy owner）的角色、而不是执行查询者的角色来求值策略表达式，所以查询者不需要映射表的访问权限，策略照样能查映射表决定返回哪些行。建议把集中式映射表和受保护表放在同一个数据库中，尤其当策略调用 `IS_DATABASE_ROLE_IN_SESSION` 时。
