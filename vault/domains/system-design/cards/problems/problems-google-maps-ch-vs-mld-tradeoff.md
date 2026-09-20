---
id: problems-google-maps-ch-vs-mld-tradeoff
node: problems.geo.google-maps
type: qa
step: 4
tags: [grown]
---
## Q
When a road-routing engine needs to incorporate live traffic updates, why might a design choose a partitioned hierarchical method (Multi-Level Dijkstra / Customizable Route Planning-style, as used by OSRM) over plain Contraction Hierarchies (CH), even though plain CH gives faster individual queries?

## A
Plain CH's shortcuts and node-importance ordering are computed from the graph's edge weights (travel times), so when live traffic changes those weights across the network, correctness in principle requires re-running the whole contraction preprocessing — an offline batch job that can take on the order of an hour on a large road network, far slower than the minute-level freshness live traffic needs. A partitioned method instead divides the graph into cells and only precomputes shortcuts between each cell's boundary nodes; when traffic changes edge weights, only the affected cells' boundary shortcuts need to be recomputed ('customized'), which is fast enough to run frequently. The trade-off is that partitioned queries are somewhat slower than pure CH queries (though still millisecond-scale), in exchange for being able to absorb live traffic changes without a full preprocessing rebuild.

## Q zh
当一个路径规划引擎需要接入实时路况更新时，为什么设计可能会选择一种分区式的分层方案（类似 Multi-Level Dijkstra / Customizable Route Planning，OSRM 所采用的方式），而不是纯粹的 Contraction Hierarchies（CH），即便纯 CH 的单次查询更快？

## A zh
纯 CH 的捷径边和节点重要性排序都是基于图的边权重（通行时间）算出来的，一旦实时路况让网络里的这些权重整体改变，理论上要保证正确性就需要重新跑一遍完整的收缩预处理——这是一个离线批处理，在大规模路网上可能要花上小时级的时间，远跟不上实时路况要求的分钟级新鲜度。分区式方案则把图划分成若干分区（cell），只预计算每个分区边界节点之间的捷径；路况改变边权重时，只需要重新计算（customize）受影响分区的边界捷径，这个开销小到可以频繁执行。代价是分区式查询比纯 CH 查询略慢（但仍是毫秒级），换来的是不需要整体重建预处理就能吸收实时路况变化。
