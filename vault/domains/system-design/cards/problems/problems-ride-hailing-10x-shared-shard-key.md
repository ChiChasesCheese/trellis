---
id: problems-ride-hailing-10x-shared-shard-key
node: problems.geo.ride-hailing
type: qa
step: 7
tags: [grown]
---
## Q
At 10x scale (daily trips growing from 40 million to 400 million, peak location-ingestion QPS growing to roughly 3.6 million), the location ingestion pipeline and the spatial index must be sharded geographically. Why must the matching service's shard routing use the same hierarchical cell ID (S2 or H3) as both the ingestion shard key and the matching query key, rather than choosing shard keys independently for each?

## A
If ingestion and matching used different, independently-chosen shard keys, a matching request for a given area could no longer assume that all of the relevant drivers' latest locations live in one place — it would have to query and merge results across shards just to answer a single geographic query, on every request. Using the same hierarchical cell ID as the shard key for both ingestion writes and matching reads means a driver's location update and a matching query for that driver's area land on the same shard, so a typical (non-boundary) matching query only needs to read from one shard instead of fanning out and merging across the whole cluster.

## Q zh
在 10 倍规模下（日行程数从 4,000 万涨到 4 亿，峰值位置摄入 QPS 涨到约 360 万），位置摄入管道和空间索引都必须按地理区域分片。为什么撮合服务的分片路由必须和位置摄入用同一个层级单元 ID（S2 或 H3）作为分片键，而不能各自独立选择分片键？

## A zh
如果摄入和撮合各自独立选择分片键，某个区域的撮合请求就不能再假设该区域相关司机的最新位置都在同一个地方——每一次查询都要跨分片查询并合并结果，才能回答一个本来只是单一地理范围的问题。用同一个层级单元 ID 同时作为摄入写入和撮合查询的分片键，意味着一个司机的位置更新和针对他所在区域的撮合查询会落在同一个分片上，这样一次典型（非边界）撮合查询只需要读一个分片，而不需要跨整个集群扇出再合并。
