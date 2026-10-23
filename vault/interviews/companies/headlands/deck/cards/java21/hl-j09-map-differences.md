---
id: hl-j09-map-differences
node: java21.j09-sequenced-collections
type: qa
step: 12
---
## Q
`SequencedMap` 与 `SequencedCollection` 有哪两点不同？怎么修改 `firstEntry()` 拿到的条目的值？

## A
1. `firstEntry()` / `pollFirstEntry()` 空时**返回 `null`**（沿用 `NavigableMap`），不抛异常；而 `SequencedCollection.getFirst()` 空时抛 `NoSuchElementException`。
2. 返回的 `Entry` 是**只读快照**：`m.firstEntry().setValue(99)` 抛 `UnsupportedOperationException`（`LinkedHashMap`、`TreeMap` 都是）。

改值用 `m.put(key, newValue)`。写 `m.firstEntry().getKey()` 前要判 null。
