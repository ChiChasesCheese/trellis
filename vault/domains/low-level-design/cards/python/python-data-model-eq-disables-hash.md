---
id: python-data-model-eq-disables-hash
node: python.data-model
type: qa
step: 1
tags: [grown]
---
## Q
一个类只重写了 `__eq__`，没有重写 `__hash__`，会出现什么问题？为什么会这样？

## A
Python 会自动把这个类的 `__hash__` 设为 `None`——类变得**不可哈希（unhashable）**，放进 `set` 或用作 `dict` 的 key 会抛 `TypeError`。原因是数据模型（data model）的约定：默认的 `__eq__`/`__hash__` 都基于对象身份（`id()`），一旦你重定义了“相等”的含义却没有同步给出新的哈希实现，Python 认为继续沿用基于身份的旧哈希是不安全的（相等的两个对象哈希不同，会破坏 `dict`/`set` 的不变式），于是干脆禁用它，逼你显式做出决定。
