---
id: protocol-structural-vs-nominal-subtyping
node: classes.abc-protocols
type: qa
source: python-docs
---
## Q
`typing.Protocol` 提供的「结构化子类型（structural subtyping）」和普通继承的「名义子类型（nominal subtyping）」有什么本质区别？

## A
名义子类型下，类 `A` 要被当作类 `B` 的子类型，必须显式地 `class A(B)` 声明继承关系——哪怕 `A` 已经实现了 `B` 要求的全部方法。结构化子类型下（`typing.Protocol` 的做法），完全不需要显式继承：只要一个类恰好定义了 `Protocol` 子类要求的方法签名（比如都有 `def meth(self) -> int`），静态类型检查器就认为它满足这个协议，可以传给要求该 `Protocol` 类型的函数——这更贴近 Python 原生的鸭子类型（duck typing）风格，不强迫写 `class Bucket(Sized, Iterable[int])` 才能通过类型检查。
