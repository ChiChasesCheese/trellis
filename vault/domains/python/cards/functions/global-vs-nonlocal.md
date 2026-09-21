---
id: global-vs-nonlocal
node: functions.scope-closure
type: qa
source: python-docs
---
## Q
要在函数内部修改外层作用域的变量，`global` 和 `nonlocal` 分别适用于什么情况？两者都不声明会发生什么？

## A
`global x` 让赋值直接作用于模块级（global）命名空间；`nonlocal x` 让赋值作用于最近一层外层函数（enclosing function）的命名空间，只能用在嵌套函数里，且要求该名字已在某个外层函数作用域存在，否则编译期报 `SyntaxError`。两者都不声明时，函数内对该名字的赋值只会在当前函数的局部作用域新建一个同名变量，外层变量保持不变——即读时可见，写时被遮蔽。
