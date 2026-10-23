---
id: hl-j02-abstract-parent-variant
node: java21.j02-sealed
type: qa
step: 15
---
## Q
为什么说"`sealed` 的父类如果不是抽象类，它自己也算一种变体"？举例说明会导致什么编译错误，怎么修。

## A
`sealed class Option`（非抽象）本身可以 `new Option()`，所以它是一个**具体的变体**。

`switch` 若只有 `case CallOption`、`case PutOption`，编译失败：`the switch expression does not cover all possible input values`。

两种修法：补一个 `case Option`；或把 `Option` 改成 `abstract`，这样只剩 `CallOption`、`PutOption`，就穷尽了。

接口天然没有直接实例，没有这个问题。
