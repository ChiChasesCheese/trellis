---
id: hl-j09-hierarchy
node: java21.j09-sequenced-collections
type: qa
step: 4
---
## Q
Java 21 新增的三个 Sequenced 接口是什么？现有的 `List`、`Deque`、`LinkedHashSet`、`TreeSet`、`LinkedHashMap`、`TreeMap` 各挂在哪个接口下？

## A
新增 `SequencedCollection`、`SequencedSet`、`SequencedMap`。

- `SequencedCollection`（继承 `Collection`）：`List`、`Deque` 现在都是它。
- `SequencedSet` = `Set` + `SequencedCollection`：`LinkedHashSet`，以及 `SortedSet` → `NavigableSet` → `TreeSet`。
- `SequencedMap`（继承 `Map`）：`LinkedHashMap`，以及 `SortedMap` → `NavigableMap` → `TreeMap`。

层级是把**已有的接口和类接上去**，不需要改已有代码：`ArrayList` 自动就是 `SequencedCollection`，`TreeMap` 自动就是 `SequencedMap`。这是纯库改动，没有新语法。
