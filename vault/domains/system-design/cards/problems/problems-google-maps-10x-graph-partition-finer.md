---
id: problems-google-maps-10x-graph-partition-finer
node: problems.geo.google-maps
type: qa
step: 8
tags: [grown]
---
## Q
In a Google Maps-style routing design, if the size of the in-memory, region-partitioned road graph grows roughly 10x (for example, by adding pedestrian paths and trails to a graph that previously only had drivable roads), what has to change about the graph's partitioning, and what tension does that create?

## A
Each geographic partition has to become finer-grained so the graph for any single partition still fits comfortably in one node's memory, since the coarser partitioning that worked at the smaller scale would now produce partitions too large to hold in RAM. This creates a direct tension in choosing partition granularity: partitions that are too coarse don't fit in memory, but partitions that are too fine increase the number of cross-partition boundary queries and the overhead of merging results across partition boundaries — the same granularity trade-off that governs how finely a partitioned hierarchical routing index (like Multi-Level Dijkstra) divides the graph in the first place.

## Q zh
在一个类 Google Maps 的路径规划设计中，如果常驻内存、按区域分区的路网图规模涨到约 10 倍（比如把此前只包含可驾驶道路的图，扩展到也包含步行道和小径），路网图的分区方式需要怎么变？这会带来什么样的张力？

## A zh
每个地理分区必须切得更细，才能保证单个分区的图仍然能舒服地放进一台节点的内存——在更小规模下够用的粗粒度分区，现在会产生大到内存装不下的分区。这在分区粒度的选择上造成直接的张力：分区太粗会放不进内存，分区太细则会增加跨分区边界查询的数量和跨分区合并结果的开销——这正是决定分层路径规划索引（比如 Multi-Level Dijkstra）一开始该把图切多细的同一种粒度取舍。
