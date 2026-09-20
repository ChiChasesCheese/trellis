---
id: python-protocol-structural
node: python.protocols-abc
type: qa
step: 1
tags: [grown]
---
## Q
`typing.Protocol` 的“结构化子类型（structural subtyping）”具体是什么意思？一个类需要显式声明“实现”某个 Protocol 吗？

## A
不需要。只要一个类拥有 Protocol 要求的方法/属性（名字和签名匹配），静态类型检查器（如 mypy）就认为它满足这个 Protocol——这是“鸭子类型的静态版本”：类型兼容性由**形状（结构）**决定，不是由继承关系声明的。定义 Protocol 的一方和实现它的一方可以完全互不知情、不互相 import，很适合给标准库/第三方类型“补”一个接口。
