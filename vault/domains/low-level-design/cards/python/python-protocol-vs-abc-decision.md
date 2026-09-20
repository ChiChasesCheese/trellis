---
id: python-protocol-vs-abc-decision
node: python.protocols-abc
type: qa
step: 5
tags: [grown]
---
## Q
面试里被问“这个接口用 `Protocol` 还是 `abc.ABC`”，怎么决策？

## A
看两件事：**是否拥有实现方的代码**，以及**是否需要共享实现/强制约束**。要给标准库/第三方类型、或调用方尚未写出的类型补一个接口，只能用 `Protocol`（结构化，不需要它们继承你的类）。如果接口的实现者都在自己的代码里，并且想在基类里放共享逻辑、或者想让“忘记实现某方法”在实例化时就报错而不是运行到那一行才 `AttributeError`，`ABC` 更合适。
