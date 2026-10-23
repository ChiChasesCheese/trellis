---
id: hl-cache-qa-tree-list-array
node: foundations.cpu-cache-locality
type: qa
step: 38
---
## Q
追问：二叉树、链表、数组，在 CPU 眼里区别是什么？

## A
推荐答法：「数组连续，预取友好；链表和树是指针追逐，每步依赖上一步的地址，无法预取，每个节点潜在一次缓存缺失。所以 n 不大时，排好序的数组加二分常赢过 `TreeMap`。」

数字：`TreeMap.get` 215 ns，`HashMap.get` 10 ns。
