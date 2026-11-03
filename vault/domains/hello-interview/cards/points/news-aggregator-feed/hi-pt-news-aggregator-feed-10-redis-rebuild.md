---
id: hi-pt-news-aggregator-feed-10-redis-rebuild
node: qb.sd.news-aggregator-feed.points
type: qa
step: 10
---
## Q
**新闻聚合系统 · Redis 索引的体量与重建**｜追问 · 出自：新闻聚合系统 › 取舍与追问

追问：分类索引放 Redis，内存要多少？丢了怎么办？数据库怎么选？

## A
**数字。** 每分类 1000 条 × 约 40 字节（ID + score）≈ 40 KB，一万个分类约 400 MB。
**重建。** 索引只是加速层，丢了可从文章库按 `published_at` 重建。
**选型。** 文章按主键读写、无跨文章事务，用键值/宽列库。
