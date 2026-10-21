---
id: amz-closest-store-followup-range-constraint-fenwick
node: amazon.amz-closest-store
type: qa
step: 6
tags: [grown]
---
## Q
在 Amazon 增删查最近值设计里，面试官追加「所有值都落在 [lo, hi] 内」。该改哪里、哪些类保持不动？树状数组怎么找前驱？

## A
只新增 `FenwickIndex(lo, hi)` 一个类实现 `OrderedIndex`，`NumberStore` 和测试不动。前驱 `floor(x)`：求前缀个数 k，k 为 0 则无前驱，否则取全集第 k 小的值（树上倍增下降）。例：值域 1..8 插入 2、3、3、7，`floor(5)` 得 3，`ceiling(5)` 得 7。
