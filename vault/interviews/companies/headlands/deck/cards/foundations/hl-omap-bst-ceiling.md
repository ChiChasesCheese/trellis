---
id: hl-omap-bst-ceiling
node: foundations.ordered-maps-trees
type: qa
step: 5
---
## Q
在 BST 里怎么求 `ceilingKey(x)`（≥ x 的最小 key）？在根 50、左 30（20, 40）、右 70（60, 80）的树里求 `ceiling(55)`。

## A
做法：像查找 x 一样走，**每次向左拐时记下当前节点**，最后一次记下的就是答案。

`ceiling(55)`：50 → 55 > 50 向右（不记）；70 → 55 < 70 向左（记 70）；60 → 55 < 60 向左（记 60）；60 的左孩子为空，结束。答案 **60**。

对称地，`floorKey(x)` 是每次向右拐时记下当前节点。
