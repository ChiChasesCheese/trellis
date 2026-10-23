---
id: hl-omap-calc-bst-build
node: foundations.ordered-maps-trees
type: qa
step: 39
---
## Q
依次向空 BST 插入 50, 30, 70, 20, 40, 60, 80, 65，65 落在哪里？中序遍历是什么？在这棵树里 `floorKey(62)` 和 `ceilingKey(62)` 是多少？

## A
65 > 50 去右，65 < 70 去左，65 > 60 成为 60 的右孩子。中序遍历（左-根-右）：20 30 40 50 60 65 70 80，升序。

查 62 的路径：50（62 > 50 向右，floor 候选 50）→ 70（62 < 70 向左，ceiling 候选 70）→ 60（向右，floor 候选 60）→ 65（62 < 65 向左，ceiling 候选 65）→ 65 的左孩子为空，结束。**`floorKey(62)` = 60，`ceilingKey(62)` = 65。**
