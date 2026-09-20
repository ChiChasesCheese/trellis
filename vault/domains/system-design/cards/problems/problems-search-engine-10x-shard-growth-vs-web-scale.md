---
id: problems-search-engine-10x-shard-growth-vs-web-scale
node: problems.search.search-engine
type: qa
step: 8
tags: [grown]
---
## Q
In a post-search design scaling from 500M to 5 billion DAU (10x), the inverted index shard count grows from about 32 to about 320 (linear with the index size, which scales with post volume). Why is 320 still comfortably below the ~480 shards estimated for a web-scale search engine, and what does that comparison suggest about document partitioning's headroom?

## A
The web-scale estimate (~480 shards) came from a much larger assumed corpus (20 billion pages) with far more indexable terms per document (about 800 for long pages vs. 18 for short posts), not from a fundamentally different partitioning strategy. Since post search at 10x growth (320 shards) still lands below that web-scale figure, document partitioning has meaningful headroom to keep scaling by simply adding shards before the fan-out width and its associated tail-latency risk reach the range already shown to be survivable (with hedged requests) at web scale.

## Q zh
在一个从 5 亿日活扩展到 50 亿日活（10 倍）的站内帖子搜索设计中，倒排索引分片数从约 32 增长到约 320（与索引大小同比例增长，而索引大小又和发帖量成正比）。为什么 320 依然明显低于网页搜索规模估算出的约 480 个分片？这个对比说明了按文档分片这个策略还有多少扩展空间？

## A zh
网页搜索规模估算出的约 480 个分片，来自一个假设大得多的语料（200 亿网页）和每篇文档多得多的可索引词项（长网页约 800 个，短帖子约 18 个），而不是因为用了根本不同的分片策略。既然站内帖子搜索 10 倍增长后（320 个分片）依然低于这个网页搜索的数字，说明按文档分片这个策略还有相当的扩展空间——可以继续单纯靠加分片来扩容，直到扇出宽度和随之而来的长尾延迟风险逼近网页搜索规模那个已经证明（借助对冲请求）可以承受的区间。
