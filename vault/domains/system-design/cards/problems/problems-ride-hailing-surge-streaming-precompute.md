---
id: problems-ride-hailing-surge-streaming-precompute
node: problems.geo.ride-hailing
type: qa
step: 4
tags: [grown]
---
## Q
In a ride-hailing design with roughly 1,389 peak ride-request QPS, why does surge pricing use a separate streaming pipeline that continuously aggregates supply and demand per geographic cell and caches a multiplier, rather than computing the supply/demand ratio fresh on every ride request?

## A
The supply/demand ratio for a region is computed from an aggregation over a recent time window of driver locations and open orders, and that aggregate barely changes on a timescale of a few seconds — so if every one of the ~1,389 peak requests per second recomputed it from scratch, the system would be repeating the same expensive aggregation for a result that is almost always identical to the previous request's answer. Decoupling computation from lookup — a streaming pipeline (Kafka ingesting trip and location data, aggregated per H3 cell, e.g. by Flink) continuously updates a region-to-multiplier cache, and a ride request just does one fast key lookup against it — turns a rarely-changing, expensive-to-compute value into a cheap read, the same pattern as precomputing a read-heavy index instead of recomputing it per query.

## Q zh
在一个峰值撮合请求约 1,389 QPS 的网约车设计中，为什么动态定价（surge pricing）用一条独立的流式管道持续按地理单元聚合供需并缓存一个倍率，而不是在每次叫车请求时都重新计算供需比？

## A zh
一个区域的供需比是对最近一段时间窗口内的司机位置和未完成订单做聚合算出来的，这个聚合结果在几秒钟的时间尺度上几乎不会变化——所以如果峰值每秒约 1,389 次请求都从头重新计算一遍，系统就是在为一个几乎总是和上一次请求答案相同的结果，重复执行同一次昂贵的聚合。把计算和查询解耦——一条流式管道（Kafka 摄入行程和位置数据，按 H3 单元聚合，例如用 Flink）持续更新一份'区域到倍率'的缓存，叫车请求只做一次快速的键查找——把一个变化很慢、计算代价很高的值变成了廉价的读取，和'预计算一个读多的索引而不是每次查询都重算'是同一个模式。
