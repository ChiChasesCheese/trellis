---
id: compile-error-stage-diagnosis
node: query.compilation-pipeline
type: qa
tags: [grown]
---
## Q
Snowflake 查询失败时，如何根据失败发生在哪个阶段判断问题类型？为什么 Query History 里有些失败查询的 SQL 显示为 `<redacted>`？

## A
解析（parse）阶段失败是语法错误；绑定（bind）阶段失败是对象不存在、列名写错或当前角色无权限；执行阶段失败才是运行时问题（如类型转换失败、除零、超时）。前两类在编译期就被拒绝，还没用到仓库资源。因语法或解析错误而失败的查询，在 Query History 中默认以 `<redacted>` 代替原始 SQL 文本，拥有相应权限的角色可以设置 `ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR` 参数查看完整文本。
