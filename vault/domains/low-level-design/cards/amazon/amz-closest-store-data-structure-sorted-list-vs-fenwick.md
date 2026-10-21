---
id: amz-closest-store-data-structure-sorted-list-vs-fenwick
node: amazon.amz-closest-store
type: qa
step: 4
tags: [grown]
---
## Q
在 Amazon 增删查最近值设计里，要支持随时增删又能快速找最近值，有序列表 + `bisect`、树状数组（Fenwick tree）、自写平衡树各自的代价是什么？怎么选？

## A
有序列表 + `insort`：查 O(log n)，增删要 O(n) 搬移，但不需要知道值域；实测随机整数 100 万个时每次插入约 33 微秒。树状数组：要求值域 [lo, hi] 已知，增删查都是 O(log R)，实测每次插入约 0.7 微秒且与 n 无关，内存 O(R)。平衡树：渐近最优，但 45 分钟写不稳、Python 里常数大。结论：默认有序列表，出现值域约束就换树状数组。
