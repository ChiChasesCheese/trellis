---
id: uth-cpp-map-set-1-rbtree
node: cpp.map-set
type: qa
step: 1
---
## Q
**map 与 set 底下是什么**｜C++ · libstdc++ 16

`std::map` / `std::set` 为什么遍历出来是有序的，查找是 O(log n)？

## A
**结构。** 红黑树（red-black tree）：每个节点存父、左、右三个指针和一位颜色。

**细节。**

- 树根旁的头节点还记着最左、最右节点和元素个数，所以 `begin()` 是 O(1)
- 中序遍历就是有序遍历，`lower_bound` 沿树下降 O(log n)
- 插入、删除靠旋转和变色保持平衡，最长路径不超过最短路径的 2 倍
- Java 的 `TreeMap` 也是红黑树

**为什么。** 比 AVL 树平衡得松，插入最多只需两次旋转，适合频繁插入删除；比哈希表多了有序和范围查询。

**对应 LeetCode：** LC 729 我的日程安排表 I · LC 220 存在重复元素 III
