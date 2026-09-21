---
id: lambda-refactor-rule
node: functions.first-class
type: qa
source: python-docs
---
## Q
一段 `lambda` 表达式越写越复杂（嵌套条件表达式、配合 `functools.reduce` 处理元组）时，除了直接看不懂，工程上还有什么代价？应该怎么重构？

## A
复杂 lambda 不能拆成多行调试、不能加类型注解，报错栈里只显示 `<lambda>` 没有语义名字，难以定位出错位置。推荐的重构步骤：先写出 lambda，用注释说明它做什么，从注释提炼出一个名字，把它改写成同名的 `def` 函数，再删掉注释；多数 `functools.reduce(lambda...)` 的场景改写成 `for` 循环或 `sum()` 配合生成器表达式反而更清楚。
