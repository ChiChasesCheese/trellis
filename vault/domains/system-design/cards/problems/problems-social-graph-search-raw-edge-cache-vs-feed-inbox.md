---
id: problems-social-graph-search-raw-edge-cache-vs-feed-inbox
node: problems.social.social-graph-search
type: qa
step: 4
tags: [grown]
---
## Q
In a social graph design, a read-through cache in front of the sharded edge store can hold the entire graph (hundreds of gigabytes) rather than only a 'hot' subset. Why does a cache miss here cost far less than a cache miss in a follow-based news feed's per-user inbox cache?

## A
The graph cache stores raw edges — a cache miss just means issuing one indexed point read against the owning shard, which is cheap and requires no further computation. A news feed's inbox cache stores a precomputed, ranked view of content assembled from many followees; a miss there means reconstructing that ranked view by aggregating and scoring content from potentially thousands of followed accounts, which is a genuinely expensive computation, not a single lookup. The difference is caching raw source data versus caching an expensive derived aggregate.

## Q zh
在一个社交关系图设计里，架在分片边存储前面的读穿缓存可以缓存整张图（几百 GB 级），而不只是「热门」的一小部分。为什么这里的一次缓存未命中，代价远低于基于关注关系的信息流里按用户收件箱缓存的一次未命中？

## A zh
图缓存存的是原始边——一次未命中只是对拥有该数据的分片发一次索引点查询，很便宜，不需要任何进一步的计算。信息流的收件箱缓存存的是从很多个被关注对象聚合而来的、预先算好排序的内容视图；那里的一次未命中意味着要重新聚合并打分可能成千上万个被关注账号的内容来重建这份排序视图，是真正昂贵的计算，不是一次简单查找。区别在于缓存原始源数据，还是缓存一份代价高昂的衍生聚合结果。
