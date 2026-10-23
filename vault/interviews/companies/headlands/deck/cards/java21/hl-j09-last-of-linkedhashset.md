---
id: hl-j09-last-of-linkedhashset
node: java21.j09-sequenced-collections
type: qa
step: 29
---
## Q
Java 21 之前和之后，怎么取 `LinkedHashSet` 的最后一个元素？复杂度各是多少？

## A
- **之前**：遍历到底 O(n)（或 `new ArrayList<>(set)` 再取，也是 O(n)）；
- **现在**：`set.getLast()` 直接读内部链表尾，**O(1)**。

这就是 Sequenced Collections 解决的痛点之一：`LinkedHashSet` / `LinkedHashMap` 内部维护双向链表，旧 API 却不给取尾部的办法。
