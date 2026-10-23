---
id: hl-heap-what-for
node: foundations.heap-priority-queue
type: qa
step: 1
---
## Q
堆（heap）擅长什么、不擅长什么？

## A
**擅长一件事**：不停地问「现在最小（或最大）的是谁」，并且插入新元素、取走最小元素都很快（O(log n)）。

**不擅长**：不能按顺序遍历、不能按值快速查找、不能快速删除中间元素。很多 `PriorityQueue` bug 来自把它当「自动排序的列表」。
