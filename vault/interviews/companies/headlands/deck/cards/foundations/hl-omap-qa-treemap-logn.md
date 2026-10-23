---
id: hl-omap-qa-treemap-logn
node: foundations.ordered-maps-trees
type: qa
step: 34
---
## Q
面试题：`TreeMap` 为什么是 O(log n)？

## A
推荐答法：「底层是红黑树。五条规则保证最长路径不超过最短路径的两倍，高度不超过 2 log₂(n+1)。`get` / `put` / `remove` 沿一条根到叶的路径走，最多 O(log n) 步；插入删除后用最多常数次旋转加 O(log n) 次重染色恢复规则。」
