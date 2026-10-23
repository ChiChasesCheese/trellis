---
id: hl-heap-when-to-use
node: foundations.heap-priority-queue
type: qa
step: 31
---
## Q
什么需求用 `PriorityQueue`，什么需求该换别的结构？

## A
- 反复取最小 / 最大、增量插入 → **`PriorityQueue`**；
- K 路归并、事件模拟（按时间触发）、定时器 → `PriorityQueue`；
- 最大的 k 个 → 大小为 k 的**小根堆**；
- 需要有序遍历、范围查询、前驱 / 后继 → `TreeMap`，不是堆；
- 按 id 取消或改优先级 → 索引堆，或 `TreeMap` + `HashMap`，或懒删除；
- 键是有界小整数 → 桶数组（计数排序式），O(1)；
- 多线程竞争同一个队列 → `PriorityBlockingQueue` 或「单线程 + 队列」模式。
