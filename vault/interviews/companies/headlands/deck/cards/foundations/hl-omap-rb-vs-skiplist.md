---
id: hl-omap-rb-vs-skiplist
node: foundations.ordered-maps-trees
type: qa
step: 19
---
## Q
红黑树（`TreeMap`）与跳表（`ConcurrentSkipListMap`）在最坏复杂度、实现、并发、内存、范围扫描、单线程速度上怎么对比？

## A
- 最坏复杂度：红黑树 **O(log n) 保证**；跳表期望 O(log n)，最坏 O(n)（概率极小）；
- 实现：红黑树高（旋转、case 分析）；跳表低（链表 + 抛硬币）；
- 修改的局部性：旋转 / 重染色可能影响到根；跳表只改前驱的几个指针；
- 并发：红黑树难做无锁，通常整棵树加锁；跳表**容易做成无锁**（CAS）；
- 内存：红黑树每节点 3 个指针 + 颜色；跳表平均每节点 2 个 next 指针 + 索引节点；
- 范围扫描：红黑树中序遍历要回溯；跳表在第 0 层顺着链表走，很快；
- 单线程 put：`TreeMap` 约 230 ns，`ConcurrentSkipListMap` 约 390 ns。
