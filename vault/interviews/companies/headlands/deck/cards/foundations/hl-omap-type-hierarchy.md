---
id: hl-omap-type-hierarchy
node: foundations.ordered-maps-trees
type: qa
step: 20
---
## Q
`TreeMap` 和 `ConcurrentSkipListMap` 的接口层次是什么？声明变量应该写什么类型？

## A
`Map` → `SequencedMap`（Java 21）→ `SortedMap`（`firstKey`、`lastKey`、`headMap`、`tailMap`、`subMap`、`comparator`）→ `NavigableMap`（`lowerKey` / `floorKey` / `ceilingKey` / `higherKey`、`firstEntry`、`pollFirstEntry`、`descendingMap`、带 inclusive 参数的 `headMap` / `tailMap` / `subMap`）→ 分叉：
- `TreeMap`：红黑树，非线程安全；
- `ConcurrentNavigableMap` → `ConcurrentSkipListMap`：跳表，线程安全。

声明变量写 `NavigableMap<K, V>`（要导航方法）或 `SequencedMap`（只用首尾）而不是具体类，方便换实现。
