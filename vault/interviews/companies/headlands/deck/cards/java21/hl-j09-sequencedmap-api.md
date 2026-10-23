---
id: hl-j09-sequencedmap-api
node: java21.j09-sequenced-collections
type: qa
step: 11
---
## Q
`SequencedMap<K, V>` 有哪些方法？

## A
```java
interface SequencedMap<K, V> extends Map<K, V> {
    SequencedMap<K, V> reversed();
    Map.Entry<K, V> firstEntry();       Map.Entry<K, V> lastEntry();         // 空 -> null
    Map.Entry<K, V> pollFirstEntry();   Map.Entry<K, V> pollLastEntry();     // 空 -> null；非空则删除并返回
    V putFirst(K k, V v);               V putLast(K k, V v);
    SequencedSet<K> sequencedKeySet();
    SequencedCollection<V> sequencedValues();
    SequencedSet<Map.Entry<K, V>> sequencedEntrySet();
}
```
`TreeMap` 的 `firstEntry()`、`pollFirstEntry()` 一直都有，现在也能通过 `SequencedMap` 接口调用。
