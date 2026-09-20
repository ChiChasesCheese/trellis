---
id: python-data-model-mutable-hash-trap
node: python.data-model
type: qa
step: 4
tags: [grown]
---
## Q
为什么一个字段可变（mutable）的对象通常不应该实现 `__hash__`？如果硬要哈希一个之后又被修改的对象会怎样？

## A
`set`/`dict` 在插入时按对象**当时**的哈希值把它放进某个桶（bucket）；如果对象存入后字段被修改，哈希值跟着变了，之后再按新哈希去找它就找不到——对象仍在容器的内部存储里，却变得**不可达**（既查不到，也无法正常 remove）。约定俗成的做法是：可变类保留默认的、基于身份的哈希，或者显式把 `__hash__` 设为 `None`；只有把对象设计成不可变（比如 `frozen=True`）之后，才让它可哈希。
