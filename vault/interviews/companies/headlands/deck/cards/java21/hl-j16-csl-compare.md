---
id: hl-j16-csl-compare
node: java21.j16-concurrency-primitives
type: qa
step: 23
---
## Q
`ConcurrentSkipListMap` 与 `TreeMap`、`ConcurrentHashMap`、`Collections.synchronizedSortedMap` 怎么区分？它有哪些限制？

## A
- `TreeMap`：有序，**不是线程安全**，多线程要自己加锁；
- `ConcurrentHashMap`：线程安全，**无序**；
- `Collections.synchronizedSortedMap(new TreeMap<>())`：一把大锁，竞争大时是瓶颈；
- `ConcurrentSkipListMap`：有序 + 线程安全，有 `firstEntry/lastEntry/pollFirstEntry/ceilingEntry/headMap/tailMap`（Java 21 起 `NavigableMap` 继承 `SequencedMap`）。

限制：迭代器**弱一致**（反映创建后的某些修改，不抛 `ConcurrentModificationException`）；`size()` 是 **O(n)**；key/value 不能为 `null`；`merge`、`compute*` 原子。
