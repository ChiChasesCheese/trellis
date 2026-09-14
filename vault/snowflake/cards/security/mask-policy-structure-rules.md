---
id: mask-policy-structure-rules
node: security.column-masking-policies
type: qa
source: snowflake-docs
---
## Q
编写一个 Snowflake 脱敏策略（masking policy）时，签名和数据类型有什么硬性约束？条件脱敏（conditional masking）的参数又是怎样的？

## A
一个脱敏策略由单一数据类型、一个或多个条件、一个或多个脱敏函数组成，输入和输出类型必须相同（例如不能输入 timestamp 却返回 string），并且只能挂到类型匹配的列上。条件脱敏策略有多个参数：第一个参数永远是要脱敏的列，后面的参数是用来判断是否脱敏的条件列（如 `visibility = 'Public'` 时才显示 email），所有参数列必须位于同一张表或视图中；参数列越少，运行时要求值的列越少，性能越好。
