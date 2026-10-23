---
id: hl-j09-wrappers
node: java21.j09-sequenced-collections
type: qa
step: 15
---
## Q
Java 21 为 Sequenced 集合新增了哪些只读包装器？为什么旧的 `unmodifiableCollection` 不够？

## A
- `Collections.unmodifiableSequencedCollection(c)` / `unmodifiableSequencedSet(s)` / `unmodifiableSequencedMap(m)`：只读视图，**保留"有序"类型**；
- `Collections.newSequencedSetFromMap(SequencedMap<E, Boolean>)`。

旧的 `unmodifiableCollection` 会**丢掉有序类型**。例：`unmodifiableSequencedMap(m).firstEntry()` 可用，`putLast` 抛 `UnsupportedOperationException`。
