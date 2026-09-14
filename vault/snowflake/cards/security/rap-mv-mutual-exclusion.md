---
id: rap-mv-mutual-exclusion
node: security.row-access-policies
type: qa
source: snowflake-docs
---
## Q
一张表已经基于它建了物化视图（materialized view），现在想给这张表加行级访问策略（row access policy），能行吗？同一列能同时出现在行级访问策略和脱敏策略（masking policy）的签名里吗？

## A
不能加：若已从底层表创建了物化视图，就不能再给该表添加行级访问策略；反过来，表上有行级访问策略时也不能基于它创建物化视图（策略可以直接挂在物化视图上，前提是底层表没有策略）；想在基表上设策略时可以考虑改用动态表（dynamic table）。同一列也不能同时出现在两种策略的签名中；对象同时有两种策略时，先求值行级访问策略。
