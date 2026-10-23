---
id: hl-heap-definition
node: foundations.heap-priority-queue
type: qa
step: 3
---
## Q
二叉堆（binary heap）由哪两个性质定义？堆序约束了哪些节点之间的大小关系？

## A
1. **形状性质**（shape property）：**完全二叉树**，除最后一层每层都满，最后一层的节点从左往右紧挨着，没有空位。
2. **堆序性质**（heap property）：每个节点 ≤ 它的两个孩子（小根堆，min-heap）；或每个节点 ≥ 孩子（大根堆，max-heap）。

堆序只约束**父与子**，兄弟、堂兄弟之间没有大小关系。例：小根堆 `1 / (2, 8) / 2 下挂 (5, 3)`，5 和 3 谁在左边没要求，8 比 5 大也不违规。
