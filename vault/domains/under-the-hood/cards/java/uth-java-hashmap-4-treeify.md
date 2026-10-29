---
id: uth-java-hashmap-4-treeify
node: java.hashmap
type: qa
step: 4
---
## Q
**链表长到 8 一定转红黑树吗**｜Java · OpenJDK 25

同一个桶里的链表长度达到 8 时，`HashMap` 会马上转成红黑树吗？

## A
**结构。** 不一定。转树要同时满足链长够长（`TREEIFY_THRESHOLD = 8`）和表长至少 64（`MIN_TREEIFY_CAPACITY`）。

**细节。**

- 表长不足 64 时，链表过长只触发 `resize()`，把冲突摊开。
- 实测 11 个哈希全相同的 key：第 9 次插入表长 16→32，第 10 次 32→64，第 11 次才变 `TreeNode`。

**为什么。** 树节点约是普通节点的两倍大，只给冲突严重的桶用。树先按哈希排序，哈希相同再比 `Comparable`，最坏 O(log n)。

**坑。** 键没有实现 `Comparable` 且哈希全相同时，查找仍会退化为线性。

**对应 LeetCode：** LC 146 LRU 缓存 · LC 981 基于时间的键值存储
