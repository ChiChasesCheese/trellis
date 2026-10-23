---
id: hl-javaq-f-q30-main
node: java-questions.f-concurrency
type: qa
step: 18
---
## Q
`ConcurrentHashMap` 怎么做到线程安全？和 `Collections.synchronizedMap` 有什么不同？为什么不允许 null 键 / 值？
How does `ConcurrentHashMap` achieve thread safety? How is it different from `Collections.synchronizedMap`? Why no null keys/values?

## A
一句话：Java 8+ 的 CHM——空桶用 **CAS** 放入首节点；非空桶只对**该桶的头节点** `synchronized`（细粒度锁）；读不加锁（`volatile` 读）；计数用分段 `CounterCell`。并发度 ≈ 桶数。

- **不允许 null**：并发下无法区分"key 不存在"和"key 映射到 null"（`containsKey` 之后值可能已变）；`put(k, null)` 直接抛 NPE。
- **`synchronizedMap`**：**整个 map 一把锁**，所有操作串行；迭代还要手动在 map 上同步。
- **历史**：Java 7 是 16 个 `Segment`（分段锁），Java 8 改成桶级 `synchronized` + CAS。
