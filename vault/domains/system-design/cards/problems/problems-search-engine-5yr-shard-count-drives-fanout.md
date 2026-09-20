---
id: problems-search-engine-5yr-shard-count-drives-fanout
node: problems.search.search-engine
type: qa
step: 1
tags: [grown]
---
## Q
In a post-search design serving 500M DAU where 32.5M posts/day each contribute ~216 bytes to the inverted index (18 indexable terms x 12 bytes/posting), giving about 12.81TB of postings over a 5-year searchable window, why does needing roughly 32 shards (at 400GB/shard capacity) matter more than the 12.81TB figure itself?

## A
12.81TB of raw storage is not the bottleneck on modern hardware, but the shard count it forces (~32, at a 400GB-per-shard capacity assumption) directly sets the fan-out width of every query in a document-partitioned index: a query has to be sent to all ~32 shards. That fan-out width is what determines tail-latency risk (the probability at least one shard misses its latency budget grows with shard count) — so the number that actually drives the query-serving architecture is the shard count derived from storage, not the storage size on its own.

## Q zh
在一个服务 5 亿日活的站内帖子搜索设计中，每天 3,250 万条帖子各自为倒排索引贡献约 216 字节（18 个可索引词项 × 每条 12 字节），5 年可搜索窗口的倒排表总量约 12.81TB，为什么'大约需要 32 个分片（按每分片 400GB 容量估算）'比 12.81TB 这个数字本身更重要？

## A zh
12.81TB 的原始存储量在现代硬件上算不上瓶颈，但它推导出的分片数（按每分片 400GB 容量假设约 32 个）直接决定了按文档分片的索引里每次查询的扇出宽度：一次查询必须发往全部约 32 个分片。这个扇出宽度才是决定长尾延迟风险的关键（至少一个分片超出延迟预算的概率随分片数增长）——所以真正驱动查询服务架构的数字，是从存储量推导出的分片数，而不是存储量本身。
