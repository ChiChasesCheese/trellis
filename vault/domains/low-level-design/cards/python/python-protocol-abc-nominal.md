---
id: python-protocol-abc-nominal
node: python.protocols-abc
type: qa
step: 2
tags: [grown]
---
## Q
`abc.ABC` 的“名义子类型（nominal subtyping）”和 Protocol 的结构化子类型区别在哪？`abstractmethod` 是什么时候被检查的？

## A
`ABC` 要求显式声明继承关系（`class Foo(MyABC)`）或调用 `MyABC.register(Foo)`，类型兼容性由**血统**决定，不是由形状决定。`@abstractmethod` 的检查发生在**实例化时**，不是在 import/定义类时——一个没有覆盖抽象方法的子类可以被正常定义、正常 import，只有真的 `Foo()` 的那一刻才会抛 `TypeError`。
