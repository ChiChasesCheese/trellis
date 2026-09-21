---
id: types-gradual-type-checking-const
node: types.gradual-typing
type: qa
source: python-docs
---
## Q
`typing.TYPE_CHECKING` 是什么？为什么用它能避免循环导入（import cycle）？

## A
`TYPE_CHECKING` 是一个特殊常量，静态检查器假定它为 `True`，但运行时它的值是 `False`。把只用于类型注解、导入代价大或会形成循环依赖的模块放进 `if TYPE_CHECKING: import xxx` 块，运行时这行 import 根本不会执行（不产生循环导入），而检查器做静态分析时把这个常量当 `True`，正常导入并检查那些类型。
