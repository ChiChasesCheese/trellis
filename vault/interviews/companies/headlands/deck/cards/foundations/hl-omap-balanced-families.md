---
id: hl-omap-balanced-families
node: foundations.ordered-maps-trees
type: qa
step: 8
---
## Q
AVL 树、红黑树、B 树 / B+ 树、Treap / Splay 的平衡规则和特点分别是什么？谁在用红黑树？

## A
- **AVL 树**（1962）：任何节点左右子树高度差 ≤ 1，最矮、查找最快，但插入删除旋转较多；
- **红黑树**（Bayer 1972；Guibas–Sedgewick 1978）：给节点染色，用染色规则间接限制高度；查找略慢于 AVL，插入删除旋转少（插入 ≤ 2 次，删除 ≤ 3 次）。JDK `TreeMap`、C++ `std::map`、Linux 内核调度器（CFS）都用；
- **B 树 / B+ 树**：一个节点存很多 key，所有叶子同深度，为磁盘设计，一次读一个块，树很矮，数据库索引的主力；
- **Treap、Splay** 等：随机优先级 / 自调整，实现简单，不保证最坏。
