---
id: types-protocols-vs-abc
node: types.protocols-generics
type: qa
source: python-docs
---
## Q
`Protocol` 和抽象基类（ABC，abstract base class）在类型检查上的根本区别是什么？

## A
ABC 走的是名义子类型（nominal subtyping，PEP 484 最初的模型）：一个类要被认成某接口的子类，必须显式继承它，比如 `class Bucket(Sized, Iterable[int])`。`Protocol`（PEP 544）走的是结构化子类型（structural subtyping，也叫静态鸭子类型）：只要一个类恰好实现了同名的方法/属性，哪怕完全不继承 `Protocol` 子类，静态检查器也认它满足该协议——`class Bucket:` 不写任何基类，只要有 `__len__`/`__iter__`，就能被当作 `Sized`/`Iterable[int]` 传给期望这些接口的函数。
