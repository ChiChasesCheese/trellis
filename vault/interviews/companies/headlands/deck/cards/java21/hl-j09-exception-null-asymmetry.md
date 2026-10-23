---
id: hl-j09-exception-null-asymmetry
node: java21.j09-sequenced-collections
type: qa
step: 28
---
## Q
`new ArrayList<String>().getFirst()` 和 `new TreeMap<String,Integer>().firstEntry()` 在空集合上分别会发生什么？为什么不对称？

## A
- `ArrayList.getFirst()`：抛 **`NoSuchElementException`**；
- `TreeMap.firstEntry()`：返回 **`null`**。

两者来自不同传统：`SequencedCollection.getFirst` 来自 `Deque.getFirst`（抛异常），`SequencedMap.firstEntry` 来自 `NavigableMap.firstEntry`（返回 `null`）。所以写 `m.firstEntry().getKey()` 前要判 `null`。
