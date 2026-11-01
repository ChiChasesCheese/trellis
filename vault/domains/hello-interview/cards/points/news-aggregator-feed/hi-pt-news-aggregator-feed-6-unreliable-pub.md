---
id: hi-pt-news-aggregator-feed-6-unreliable-pub
node: qb.sd.news-aggregator-feed.points
type: qa
step: 6
---
## Q
**新闻聚合系统 · 出版商不可靠**｜出自：新闻聚合系统 › 深入 2

出版商超时、返回 5xx、改格式、突然吐出几千篇，怎么防止拖垮整个摄取？

## A
**熔断。** 每家一个熔断器，连续失败指数退避拉长间隔，恢复后逐步回到正常。
**限速。** 每家并发 1、每次最多处理 N 篇。
**排查。** 解析失败的原始内容进死信队列；告警看「超过 X 倍间隔未成功」的出版商数量。
