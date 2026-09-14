---
id: mask-query-time-not-static
node: security.column-masking-policies
type: qa
source: snowflake-docs
---
## Q
Snowflake 的动态数据脱敏（Dynamic Data Masking）会修改表里存储的敏感数据吗？分析师和客服看到同一列的不同结果是怎么实现的？

## A
不会修改，存储的仍是明文，没有静态脱敏（static masking）。脱敏策略（masking policy）是模式级对象，挂在列上；查询运行时 Snowflake 改写查询，对该列套用策略表达式，根据条件（如 `CURRENT_ROLE`、`IS_ROLE_IN_SESSION` 或查授权表）决定返回原值、部分脱敏值、混淆值还是令牌。于是 ANALYST 角色只看到手机号后四位，SUPPORT 角色看到完整号码，底层数据是同一份。
