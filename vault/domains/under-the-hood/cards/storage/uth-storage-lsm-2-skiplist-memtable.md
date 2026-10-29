---
id: uth-storage-lsm-2-skiplist-memtable
node: storage.lsm
type: qa
step: 2
---
## Q
**内存表为什么是跳表**｜RocksDB · v10.9

RocksDB 的内存表默认用什么数据结构？为什么不用红黑树？

## A
**结构。** 默认 `SkipListFactory`：跳表，最多 12 层，每层以 1/4 的概率向上长（`branching_factor = 4`），平均每个元素约 1.33 个指针。

**细节。**

- 多线程可以并发插入（`allow_concurrent_memtable_write`，默认开启），但只有跳表实现支持。
- 有序遍历就是顺着最底层链表走，刷成 SST 时按序直接写出，不用再排序。

**为什么。** 跳表插入只改局部的几个指针，容易做成无锁并发；平衡树的旋转要同时改好几个节点，并发实现麻烦得多。

**对应 LeetCode：** LC 1206 设计跳表
