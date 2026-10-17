---
id: amz-occupancy-tracker-decision-range-max-start-count-and-segment-tree
node: amazon.amz-occupancy-tracker
type: qa
step: 5
tags: [grown]
---
## Q
在办公室人数追踪里，`max_in(a, b)` 该怎样算？区间最大值用什么结构？

## A
答案是两部分取最大：区间开始时已在楼里的人数 `count_at(a)`，与区间内每个事件之后的人数。后者是前缀和数组的一段连续下标，求这段最大值有三个选项：扫描 O(k)，最简单；稀疏表查询 O(1)，但追加要重建；线段树查询 O(log n)、追加摊还 O(1)。选线段树，因为持续追加又要频繁查询。常见错误：漏掉 `count_at(a)`。例：`+1@10, +1@20, −1@30`，`max_in(25, 25)` 应为 2，只看区间内事件会得 0。
