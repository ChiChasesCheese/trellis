---
id: hl-j03-primitive-selector
node: java21.j03-pattern-switch
type: qa
step: 24
---
## Q
Java 21 里选择器是 `int` 时能不能写 `case Integer i`？怎么办？

## A
不能：Java 21 里模式 `switch` 的选择器必须是**引用类型**，对 `int` 选择器用 `case Integer i` 报 `pattern of type Integer is not applicable at int`。

办法：先装箱成 `Integer` / `Object`，或用传统的常量标签。
