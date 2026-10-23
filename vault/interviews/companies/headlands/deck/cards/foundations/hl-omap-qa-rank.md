---
id: hl-omap-qa-rank
node: foundations.ordered-maps-trees
type: qa
step: 38
---
## Q
面试题：要「第 k 小」或「小于 x 的元素个数」，用 `TreeMap` 行吗？

## A
不行，`headMap(x).size()` 是 O(n)。要用 **Fenwick 树**（价格离散化后）或带子树大小的平衡树（**order-statistic tree**），做到 O(log n)。
