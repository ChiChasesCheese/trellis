---
id: hl-omap-choose-structure
node: foundations.ordered-maps-trees
type: qa
step: 31
---
## Q
不同需求下该选什么结构：只查改、保持插入顺序、有序导航、并发有序、只取最小、几乎不变的数据、有界小整数、第 k 小、超内存持久化？

## A
- 只按 key 查改、不要有序 → `HashMap`；
- 保持插入顺序遍历 → `LinkedHashMap`（`HashMap` + 双向链表）；
- 取最小 / 最大、前驱后继、范围查询、有序遍历 → **`TreeMap`**；
- 同上且多线程并发 → **`ConcurrentSkipListMap`**；
- 只要反复取最小 → `PriorityQueue`（更简单更快）；
- 数据几乎不变只查询 → 排好序的数组 + `Arrays.binarySearch`（缓存友好）；
- key 是有界小整数（如 tick 价位）→ **数组下标**配位图 / 最优价指针，O(1)；
- 「第 k 小」「小于 x 的有多少个」→ Fenwick 树 / order-statistic 树，`TreeMap` 做不到 O(log n) 的 rank；
- 数据比内存大要持久化 → B+ 树 / LSM-tree。
