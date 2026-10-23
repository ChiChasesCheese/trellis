---
id: hl-heap-perf-constants
node: foundations.heap-priority-queue
type: qa
step: 30
---
## Q
在性能敏感代码里，`PriorityQueue` 有哪些常数问题？d 叉堆（d-ary heap）为什么更快？

## A
- **装箱**：`PriorityQueue<Long>` 里每个 `Long` 是堆上对象，比较要追指针（缓存未命中）。合并多路流时把堆做成 `long[]` 加平行数组，就是为消掉这个开销。
- **d 叉堆**：二叉改 4 叉，树更矮（log₄ n = (log₂ n)/2），孩子在数组里相邻（一次缓存行读入），上浮更便宜，下沉要比 4 个孩子。高性能实现（如 Boost 的 `d_ary_heap`）常用 4 叉或 8 叉；`PriorityQueue` 是二叉。
- **价格有界的订单簿**：最优价用「数组 + 位图 / 指针」比堆更好，O(1) 找最优价、O(1) 插入。堆只在候选集合无界、没有结构可利用时才是正确选择。
- **取消订单**要按 id 删除，而堆 `remove(Object)` 是 O(n)，这是订单簿用 `TreeMap` + 价位队列而不用 `PriorityQueue` 的原因之一。
