---
id: uth-storage-inverted-index-2-skip-data
node: storage.inverted-index
type: qa
step: 2
---
## Q
**跳转数据：求交集时跳着走**｜Lucene · 10.5

一个词的文档号列表有几百万项，另一个词只有几十项，求交集时 Lucene 怎么避免把长列表扫一遍？

## A
**结构。** 列表里夹着两级跳转数据（skip data）：第 0 级在每个 256 项的块之前，第 1 级每 32 个块一条，覆盖 8192 篇文档。

**细节。**

- 以最短的列表为主驱动（`ConjunctionDISI` 按成本排序），对其他列表调用 `advance(目标文档号)`。
- `advance` 先用第 1 级跳过整段 8192 篇，再用第 0 级跳过块，最后只解码一个块。
- 对方跳过头了，主列表就跟着往前跳（leapfrog）。

**为什么。** 跳转数据就是磁盘版的跳表：求交集的代价由短列表的长度决定，不由长列表的长度决定。

**对应 LeetCode：** LC 1206 设计跳表 · LC 986 区间列表的交集
