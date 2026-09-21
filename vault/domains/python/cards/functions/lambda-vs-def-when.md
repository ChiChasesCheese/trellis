---
id: lambda-vs-def-when
node: functions.first-class
type: qa
source: python-docs
---
## Q
定义一个只用一次的小函数，什么时候该用 `lambda`，什么时候该用 `def`？`lambda` 有什么硬性限制？

## A
`lambda 参数: 表达式` 的函数体只能是单个表达式，不能写 `if...elif...else` 多分支、`try/except` 等语句；适合 `sorted`/`filter` 的 `key`、`predicate` 这类「一次性、逻辑简单」的场景。逻辑稍复杂就该用 `def` 命名函数：可读、能加文档字符串，报错栈（traceback）里也有名字方便定位。
