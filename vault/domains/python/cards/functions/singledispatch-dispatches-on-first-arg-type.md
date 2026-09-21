---
id: singledispatch-dispatches-on-first-arg-type
node: functions.functools
type: qa
source: python-docs
---
## Q
`@functools.singledispatch` 装饰的函数是按什么来决定调用哪个实现的？如果某个类型没有专门注册的实现会怎样？

## A
`singledispatch` 按调用时第一个参数的类型来分派（dispatch）到不同实现：先用 `@原函数.register` 给不同类型分别注册对应实现，调用时框架自动选中匹配第一个参数类型的那个版本。如果某个类型没有直接注册实现，会沿着它的方法解析顺序（method resolution order）向上找更通用的实现；一路找不到就退回执行最初被 `@singledispatch` 装饰的那个函数（它相当于注册给了 `object` 基类，作为兜底）。
