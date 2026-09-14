---
id: cc-performance-budget-n-vs-value-range
node: performance.budget
type: qa
tags: [grown]
---
## Q
A statement says values can be as large as 10^9 but the count of items is n ≤ 10^5. You write `count = [0] * (max_value + 1)` to bucket them by value. Why is this the wrong read of the constraints, and what should you index on instead?

## A
The complexity budget is governed by n (how many items you process), not by the range the values can take — a direct-indexing array sized to the value range allocates and touches 10^9 cells, blowing both time and memory even though n itself is small. Read '10^9' as a signal that values must be hashed or coordinate-compressed (sort the n distinct values, map each to its rank 0..n-1) before indexing, so every structure is sized O(n), not O(max_value).

## Q zh
题面说数值最大可到 10^9，但元素个数 n ≤ 10^5。你写了 `count = [0] * (max_value + 1)` 按数值分桶。为什么这是对约束的错误解读？应该按什么来做索引？

## A zh
复杂度预算由 n（你要处理的元素个数）决定，而不是由数值的取值范围决定——按取值范围开的直接索引数组要分配并触碰 10^9 个格子，时间和内存一起爆掉，尽管 n 本身很小。把"10^9"读成一个信号：数值必须先做哈希或坐标压缩（coordinate compression：把 n 个不同的值排序，各自映射到名次 0..n-1）再索引，这样每个结构的大小都是 O(n)，而不是 O(max_value)。
