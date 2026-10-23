---
id: hl-omap-weak-consistency-quiz
node: foundations.ordered-maps-trees
type: qa
step: 41
---
## Q
`ConcurrentSkipListMap` 上线程 A 遍历、线程 B 同时 `put`，A 会抛 `ConcurrentModificationException` 吗？A 一定能看到 B 刚加的元素吗？

## A
不会抛。迭代器弱一致：可能看见也可能看不见 B 在迭代创建之后的修改，但不重复、不崩溃，也不保证某个一致快照。需要一致快照就用 `TreeMap` + 外部锁，或持久化（不可变）结构。
