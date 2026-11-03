---
id: hi-pt-news-aggregator-feed-3-ingest-path
node: qb.sd.news-aggregator-feed.points
type: qa
step: 3
---
## Q
**新闻聚合系统 · 摄取路径**｜必会 · 出自：新闻聚合系统 › 整体设计

从出版商拿到文章并入库，整条写路径怎么走？写入顺序为什么重要？

## A
**路径。** 调度器按下次拉取时间把到期出版商放进队列（按出版商分区，同一家不会被并发拉取）→ 拉取节点发条件请求（`If-None-Match`/`If-Modified-Since`，304 几乎零成本）→ 解析、URL 规范化去重、指纹聚类。
**顺序。** 先写文章库，成功后再更新 Redis 分类有序集合（score = `published_at`，每类留约 1000 条），最后异步下载缩略图（URL 哈希作对象键，幂等）。数据库写失败就不进后续步骤，没有孤儿。
