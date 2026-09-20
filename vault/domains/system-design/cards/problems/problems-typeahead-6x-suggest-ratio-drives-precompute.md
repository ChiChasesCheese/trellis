---
id: problems-typeahead-6x-suggest-ratio-drives-precompute
node: problems.search.typeahead
type: qa
step: 1
tags: [grown]
---
## Q
In a typeahead design with 300M DAU where each user completes 3 searches/day but triggers about 6 debounced suggestion requests per search session, giving ~62,500 average suggestion QPS against only ~10,417 average submitted-search QPS, why does this 6x ratio push the design toward precomputing every prefix's suggestions offline rather than computing them at request time?

## A
Suggestion requests run at 6x the volume of actual search submissions and must each complete within a ~100ms budget, so any per-request work heavier than an in-memory O(prefix-length) lookup — a database query, a sort over candidates, a ranking model call — multiplied across ~62,500 average QPS would blow the latency budget. The only way to keep each request cheap regardless of that multiplier is to move all the expensive work (ranking, sorting) to an offline pipeline that precomputes each prefix's top-K candidates in advance, leaving the online path to do nothing more than a lookup.

## Q zh
在一个服务 3 亿日活的 typeahead 设计中，每个用户每天完成 3 次搜索提交，但每次搜索会话平均触发约 6 次经过节流的联想请求，得到约 62,500 的平均联想 QPS，而真正提交的搜索平均 QPS 只有约 10,417，为什么这个 6 倍的比例会把设计推向'离线预计算每个前缀的建议'而不是'请求时现算'？

## A zh
联想请求的流量是真正搜索提交量的 6 倍，且每一次都要在约 100ms 的预算内完成，所以任何比内存里一次 O(前缀长度) 查找更重的单次请求开销——查一次数据库、对候选排序、调用一次排序模型——乘上约 62,500 的平均 QPS 都会击穿延迟预算。唯一能让每次请求始终廉价、不受这个倍数影响的办法，是把全部昂贵的工作（排序、打分）挪到一条离线管道里提前算好每个前缀的 top-K 候选，在线路径只做一次查找。
