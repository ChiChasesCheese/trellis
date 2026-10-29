---
id: uth-java-concurrenthashmap-3-compound
node: java.concurrenthashmap
type: qa
step: 3
---
## Q
**ConcurrentHashMap 用起来的两个坑**｜Java · OpenJDK 25

为什么 `ConcurrentHashMap` 不允许 `null`？在 `computeIfAbsent` 里递归算斐波那契会怎样？

## A
**结构。** 每个桶头节点一把 `synchronized` 锁；`computeIfAbsent` 在持锁期间执行你传入的函数。

**细节。**

- key 和 value 都不能是 `null`，`put` 开头直接抛 `NullPointerException`（实测）。并发下 `get` 返回 `null` 就无法区分「没有」和「值为 null」。
- 递归 `computeIfAbsent(n, k -> fib(k-1) + fib(k-2))` 实测抛 `IllegalStateException: Recursive update`。
- 单个原子方法（`putIfAbsent`、`merge`）是安全的，先 `get` 再 `put` 的组合不是原子的。

**为什么。** 函数在持锁时执行，再改同一个桶会破坏结构，所以源码用占位节点（`ReservationNode`）检测重入并直接报错。

**对应 LeetCode：** LC 509 斐波那契数 · LC 70 爬楼梯
