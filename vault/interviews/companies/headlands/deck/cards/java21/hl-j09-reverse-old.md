---
id: hl-j09-reverse-old
node: java21.j09-sequenced-collections
type: qa
step: 2
---
## Q
Java 21 之前，怎么倒着遍历 `List`、`Deque`、`LinkedHashSet` / `LinkedHashMap`、`TreeMap`？

## A
- `List`：复制 + `Collections.reverse`；
- `Deque`：`descendingIterator()`；
- `LinkedHashSet` / `LinkedHashMap`：**没有办法**；
- `TreeMap`：`descendingMap()`。

Java 21 的 `reversed()` 对这些统一提供一个 O(1) 创建、不复制的倒序视图。
