---
id: hl-omap-other-traps
node: foundations.ordered-maps-trees
type: qa
step: 28
---
## Q
使用 `TreeMap` 还有哪些常见的坑（迭代、key、null、线程安全）？

## A
- **fail-fast 迭代器**：遍历时修改（除 `iterator.remove()`）抛 `ConcurrentModificationException`；遍历时删除用 `entrySet().removeIf(...)` 或 `Iterator.remove()`；
- **key 不可变**：放进去后别改变决定比较结果的字段，否则树内部顺序被破坏（同 `PriorityQueue` 的坑）；
- **`null`**：`TreeMap` 自然序下不允许 `null` key；`ConcurrentSkipListMap` 不允许 `null` key 或 value；
- **非线程安全**：多线程用 `Collections.synchronizedSortedMap` 或换 `ConcurrentSkipListMap`。
