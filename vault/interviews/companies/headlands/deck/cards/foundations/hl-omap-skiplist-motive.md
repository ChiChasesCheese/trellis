---
id: hl-omap-skiplist-motive
node: foundations.ordered-maps-trees
type: qa
step: 14
---
## Q
为什么平衡树很难做成无锁并发？跳表（skip list）的动机是什么？

## A
红黑树的旋转要同时改好几个节点的指针，重染色可能从叶子影响到根，让多线程同时插入 / 删除而不加全局锁非常难。

William Pugh 1990 年提出跳表：**用抛硬币代替复杂的平衡规则**，每次修改只动局部少量指针，天然适合无锁或细粒度锁并发。
