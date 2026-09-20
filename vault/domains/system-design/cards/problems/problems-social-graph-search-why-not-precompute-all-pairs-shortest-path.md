---
id: problems-social-graph-search-why-not-precompute-all-pairs-shortest-path
node: problems.social.social-graph-search
type: qa
step: 6
tags: [grown]
---
## Q
Why does a social graph design with 100M users avoid precomputing an all-pairs shortest-path table, and instead compute shortest paths on demand with a depth-bounded bidirectional search?

## A
The number of distinct user pairs at 100M users is about 5×10^15 — even storing a single byte per pair would run into the petabyte range, and every new edge added to the graph can change the shortest path for a large number of unrelated pairs, making the table's maintenance cost far exceed the cost of answering queries on demand. This mirrors why even offline analytics computing a single aggregate statistic like average degree of separation across a real social graph use approximate, sample-based algorithms rather than computing exact distances for every pair.

## Q zh
为什么一个 1 亿用户规模的社交图设计会避免预计算全量的两两最短路径表，转而用有界深度的按需双向搜索来计算最短路径？

## A zh
1 亿用户对应的不同用户对数量约为 5×10^15——即便每对只存 1 个字节，存储量也会达到 PB 级，而且图上每新增一条边都可能改变大量不相关用户对之间的最短路径，导致这张表的维护成本远超按需回答查询的成本。这也解释了为什么即便是离线分析真实社交图谱上「平均分隔度」这样一个单一的全局统计量，业界用的也是近似、基于抽样的算法，而不是为每一对用户计算精确距离。
