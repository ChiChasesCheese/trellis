---
id: hl-heap-qa-not-sorted-iter
node: foundations.heap-priority-queue
type: qa
step: 35
---
## Q
追问：`PriorityQueue` 迭代为什么不是有序的？

## A
推荐答法：「它只保证父不大于子，兄弟之间无序，迭代走内部数组顺序。要有序必须 `poll`，代价 O(n log n)。」
