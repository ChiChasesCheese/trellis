---
id: hi-pt-news-aggregator-feed-8-hot-category
node: qb.sd.news-aggregator-feed.points
type: qa
step: 8
---
## Q
**新闻聚合系统 · 热点分类写入**｜出自：新闻聚合系统 › 深入 4

突发新闻时同一分类涌入大量文章，Redis 的单个有序集合成了热点。怎么扩？数据库怎么分片？

## A
**做法。** 摄取节点先在内存按分类攒 100～500 ms 批量写；热门分类的有序集合按时间桶（每小时一个键）拆分，读时按桶从新到旧取。
**分片。** 数据库按 `articleId` 哈希分片，不按分类分片，因为分类是倾斜的。
