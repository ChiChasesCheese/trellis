---
id: uth-go-rust-rust-collections-3-btreemap
node: go-rust.rust-collections
type: qa
step: 3
---
## Q
**BTreeMap 为什么不是红黑树**｜Rust · std::collections

有序映射，Rust 为什么选 B 树，而不是 C++ `map` 那样的红黑树？

## A
**结构。** B 树（B-tree）：每个节点是一段连续数组，装 B-1 到 2B-1 个键，`B = 6`，也就是每节点最多 11 个。

**细节。**

- 平衡二叉树理论上比较次数最少（log₂ n），但每个元素一个堆节点、每次比较都可能缓存未命中
- B 树把分配次数减少到约 1/B
- 节点内用线性查找，期望比较 B·log n 次，比二叉树还多，实际却很快

**为什么。** 现代 CPU 上缓存未命中和堆分配比多几次比较贵得多。

**对应 LeetCode：** LC 729 我的日程安排表 I · LC 220 存在重复元素 III
