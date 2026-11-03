---
id: hi-pt-news-aggregator-feed-9-breaking-offline
node: qb.sd.news-aggregator-feed.points
type: qa
step: 9
---
## Q
**新闻聚合系统 · 突发新闻与离线弱网**｜追问 · 出自：新闻聚合系统 › 深入 5、6

突发新闻怎么更快送达？用户离线或网络差怎么办？

## A
**突发。** 权威出版商或标记「突发」的文章走高优先级队列，跳过批量攒写，触发 APNs/FCM 推送；按位置推送则摄取时打 geohash 标签，匹配用户订阅的区域，并对每用户限频。
**离线。** 客户端 SQLite 缓存最近页，先显示缓存同时用 `since=<游标>` 拉增量；订阅修改先写本地队列，联网后幂等重放；列表接口返回 `etag`，没变化回 304。
