---
id: patterns-builder-when
node: patterns.creational
type: qa
step: 4
---
## Q
Python 里，Builder 原本要解决的"参数太多、可选参数太多"问题，为什么大多数时候关键字参数就够了？

## A
`def __init__(self, size=12, cheese=True, pepperoni=False, ...)` 配合调用时用关键字传参，已经解决了"参数顺序记不住"的问题；需要基于已有实例改几个字段时，`dataclasses.replace(pizza, cheese=False)` 比手写一个 builder 更短。

Builder 真正还值回票价的场景是**分步骤、每一步都要校验**的构造——比如查询构造器每加一个 `.where()` 就要检查列名是否存在，或者要求"在调用 `.build()` 之前，半初始化的对象绝不能被外部拿到"。这类"过程本身带规则"的构造，关键字参数替代不了。
