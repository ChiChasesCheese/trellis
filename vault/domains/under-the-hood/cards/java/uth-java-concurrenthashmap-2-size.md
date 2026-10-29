---
id: uth-java-concurrenthashmap-2-size
node: java.concurrenthashmap
type: qa
step: 2
---
## Q
**ConcurrentHashMap 怎么数元素个数**｜Java · OpenJDK 25

多线程同时 `put`，`size()` 用一个原子计数器行吗？`ConcurrentHashMap` 是怎么做的？

## A
**结构。** 一个 `baseCount` 加一个 `CounterCell[]` 数组；这就是 `LongAdder` 的思路。

**细节。**

- 先 CAS 更新 `baseCount`；失败说明有竞争，就按线程随机探针选一个 `CounterCell` 单独累加。
- `CounterCell` 标了 `@Contended`，各占自己的缓存行，避免互相拖慢。
- `size()` 是 `baseCount` 加上所有单元的和，并发时只是近似值。
- 扩容多线程协助：每个线程领一段桶搬迁，每段至少 16 个。

**为什么。** 一个全局原子变量让所有线程的 CAS 撞在同一个缓存行上；分散计数把争用也分散了。

**对应 LeetCode：** LC 706 设计哈希映射 · LC 705 设计哈希集合
