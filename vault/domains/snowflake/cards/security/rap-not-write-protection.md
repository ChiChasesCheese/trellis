---
id: rap-not-write-protection
node: security.row-access-policies
type: qa
source: snowflake-docs
---
## Q
行级访问策略（row access policy）能阻止用户插入不该插入的行，或修改/删除自己能看到的行吗？用 CTAS 从受保护表建新表，新表有策略吗？

## A
不能。行级访问策略只控制查询中哪些行可见，目前不阻止插入行，也不阻止更新或删除可见行，写保护仍需靠权限授予。`CREATE TABLE … AS SELECT` 会把按策略过滤后的行写入新表，但新表本身不带行级访问策略；`CREATE TABLE … LIKE` 建出空表且不带策略；`CLONE` 出的表则映射到与源表相同（或对应克隆出的）策略。
