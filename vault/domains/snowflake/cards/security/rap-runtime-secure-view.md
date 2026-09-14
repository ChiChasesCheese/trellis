---
id: rap-runtime-secure-view
node: security.row-access-policies
type: qa
source: snowflake-docs
---
## Q
一张表挂了行级访问策略（row access policy，决定哪些行能出现在查询结果中的模式级策略对象）后，Snowflake 在查询运行时是如何过滤行的？

## A
运行时 Snowflake 先判断对象上是否挂有策略，若有则全部行都受保护；然后为该对象生成一个动态安全视图（dynamic secure view，即内联的安全视图）；把挂载策略时指定的列值绑定到策略参数上并求值策略表达式；最终只返回表达式结果为 `TRUE` 的行。表和其上的视图都挂策略时，先执行表上的策略，再按“表 → 视图1 → 视图2 …”的顺序依次执行视图上的策略。
