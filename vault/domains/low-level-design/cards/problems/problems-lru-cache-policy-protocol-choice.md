---
id: problems-lru-cache-policy-protocol-choice
node: problems.components.lru-cache
type: qa
step: 4
tags: [grown]
---
## Q
LRU 缓存里，`EvictionPolicy`（LRU/LFU 都要实现的淘汰策略接口）定义成 `typing.Protocol` 而不是 `abc.ABC`，理由是什么？

## A
`ABC` 的价值在于能提供共享的默认实现，或者需要用 `isinstance()` 在运行时强校验类型；而 `LRUPolicy` 和 `LFUPolicy` 之间没有任何值得共享的代码（一个用一条双向链表，一个用频率桶），`EvictionPolicy` 纯粹是一份“需要哪几个方法”的契约清单。用 `Protocol` 时，任何对象只要方法签名对得上（`record_insert`/`record_access`/`evict`/`remove`）就自动满足接口，不需要显式 `class LRUPolicy(EvictionPolicy)` 声明继承——测试代码想传一个临时的假策略时也不需要知道 `EvictionPolicy` 这个类存在。这是结构化子类型（鸭子类型）优于名义子类型的一个具体例子。
