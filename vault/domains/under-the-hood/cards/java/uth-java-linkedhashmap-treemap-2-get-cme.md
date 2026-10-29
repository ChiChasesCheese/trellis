---
id: uth-java-linkedhashmap-treemap-2-get-cme
node: java.linkedhashmap-treemap
type: qa
step: 2
---
## Q
**遍历 LRU 时 get 为什么会抛异常**｜Java · OpenJDK 25

对 `accessOrder = true` 的 `LinkedHashMap`，一边遍历 `keySet()` 一边对每个 key 调用 `get`，会发生什么？

## A
**结构。** 访问顺序模式下，`get` 会调用 `afterNodeAccess`，把节点移到链表尾，并让 `modCount` 加 1。

**细节。**

- 迭代器发现 `modCount` 变了，就抛 `ConcurrentModificationException`。实测正是如此。
- 所以在这种模式下，`get` 也是结构性修改，不只是读。
- 默认的插入顺序模式下，对已有 key 再 `put` 不改变顺序，`get` 也不改链表。

**为什么。** 「最近访问」就要靠改链表来记录，读操作不可能完全没有写。

**坑。** 多线程共享这样的缓存，`get` 也要加锁，不能只给 `put` 加锁。

**对应 LeetCode：** LC 146 LRU 缓存 · LC 432 全 O(1) 的数据结构
