---
id: uth-java-concurrenthashmap-1-cas-lock
node: java.concurrenthashmap
type: qa
step: 1
---
## Q
**ConcurrentHashMap 的 put 怎么加锁**｜Java · OpenJDK 25

Java 8 之后 `ConcurrentHashMap` 不再分段，`put` 一个 key 时到底锁了什么？`get` 要加锁吗？

## A
**结构。** 和 `HashMap` 一样的桶数组加链表或红黑树，但并发控制细到**单个桶**。

**细节。**

- 目标桶为空：用 CAS（`casTabAt`）直接放入新节点，不加锁。
- 桶非空：对桶头节点 `synchronized (f)`，在里面遍历链表追加或覆盖。
- `get` 完全不加锁：节点的 `val` 和 `next` 都是 `volatile`。
- 早期版本按段（`Segment`）加锁；现在只留一个不起作用的 `Segment` 类做序列化兼容。

**为什么。** 锁粒度从一段降到一个桶，两个线程只有写同一个桶才会互斥。

**对应 LeetCode：** LC 706 设计哈希映射 · LC 705 设计哈希集合
