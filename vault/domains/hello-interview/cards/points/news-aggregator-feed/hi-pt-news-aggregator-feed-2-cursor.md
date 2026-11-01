---
id: hi-pt-news-aggregator-feed-2-cursor
node: qb.sd.news-aggregator-feed.points
type: qa
step: 2
---
## Q
**新闻聚合系统 · 游标分页**｜出自：新闻聚合系统 › 核心实体与接口

信息流接口 `GET /feed?category=&cursor=` 为什么必须用游标分页，游标由什么组成？

## A
**为什么。** 顶部不断有新文章插入，offset 会让用户看到重复或漏掉。
**游标。** `published_at` + `articleId`。同一用户翻页不乱序也靠它保证。
