---
id: problems-proximity-10x-geo-sharding-boundary
node: problems.geo.proximity
type: qa
step: 8
tags: [grown]
---
## Q
At 10x scale (200 million indexed businesses, about 38GB), a single in-memory quadtree no longer fits on one machine and the index must be sharded by geographic region. Why do queries near a shard boundary need special handling, and why does a hierarchical index like S2 or H3 make that handling cheaper than plain country-based sharding?

## A
A user standing near the edge of one geographic shard may have nearby businesses that actually live in the adjacent shard, so a boundary query must be broadcast to neighboring shards and the results merged, rather than trusting a single shard's answer to be complete. With plain country-based sharding, 'neighboring' can mean querying an entire adjacent country's shard just to catch a few businesses across the border; a hierarchical index like S2 or H3 lets the shard key be a coarser-resolution cell, so a boundary query only needs to additionally query the small number of adjacent coarse cells rather than an entire neighboring region's shard.

## Q zh
在 10 倍规模下（2 亿索引商户，约 38GB），单台机器的内存四叉树装不下了，索引必须按地理区域分片。为什么靠近分片边界的查询需要特殊处理？为什么 S2 或 H3 这类层级索引处理这种情况比按国界分片更省？

## A zh
站在某个地理分片边缘的用户，附近的商户实际上可能属于相邻分片，所以边界查询必须向相邻分片广播并合并结果，而不能相信单个分片给出的答案是完整的。如果按国界分片，'相邻'可能意味着为了捕获边境线对面的少数几个商户就要查询整个相邻国家的分片；而 S2 或 H3 这类层级索引可以把分片键设为更粗一级分辨率的单元，边界查询只需要额外查询少数几个相邻的粗粒度单元，而不是相邻整个区域的分片。
