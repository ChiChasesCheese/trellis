---
id: hl-omap-cslm-semantics
node: foundations.ordered-maps-trees
type: qa
step: 29
---
## Q
`ConcurrentSkipListMap` 的迭代、批量操作、`compute` 系列、`size()` 分别有什么特殊语义？

## A
- 迭代器是**弱一致**（weakly consistent）：遍历期间别的线程的修改可能看见也可能看不见，但不抛 `ConcurrentModificationException`，也不重复返回同一元素；
- 批量操作 `putAll`、`equals`、`toArray`、`containsValue`、`clear` **不保证原子**；
- 不允许 `null` key 或 value；
- `compute` / `computeIfAbsent` / `merge` 的函数**不保证只原子地调用一次**，与 `ConcurrentHashMap` 不同，竞争失败会重试，所以函数必须无副作用；
- 返回的 `Map.Entry` 是快照，不支持 `setValue`；
- `size()` 历史上 O(n) 遍历计数，JDK 21 上 100 万条目仅约 0.1 µs，说明新版本维护了计数器，但面试里别断言，说「历史上 O(n)，现在的实现不一定，不应依赖」。
