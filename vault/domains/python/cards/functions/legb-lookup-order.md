---
id: legb-lookup-order
node: functions.scope-closure
type: qa
source: python-docs
---
## Q
在函数体内访问一个名字（name）时，Python 按什么顺序查找它的绑定？什么时候只用 3 层命名空间、什么时候会更多？

## A
顺序是 Local（当前函数）→ Enclosing（由内到外的外层函数作用域）→ Global（模块级）→ Builtin（内置命名空间），合称 LEGB。若这个函数没有嵌套在别的函数里，只有 Local/Global/Builtin 3 层；一旦嵌套在一层或多层外层函数里，就多出 Enclosing 这一层甚至更多层。作用域在代码写好时（静态）就已确定，真正的查找动作在运行时才发生。
