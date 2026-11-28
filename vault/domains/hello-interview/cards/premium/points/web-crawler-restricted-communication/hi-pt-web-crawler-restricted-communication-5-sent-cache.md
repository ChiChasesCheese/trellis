---
id: hi-pt-web-crawler-restricted-communication-5-sent-cache
node: qb.sd.web-crawler-restricted-communication.points
type: qa
step: 5
---
## Q
**无中心网络爬虫 · 已发集合只是缓存**｜必会 · 出自：无中心网络爬虫 › 深入 2

无中心爬虫里，每个节点记录"已经转发给别人的 URL"（已发集合）来省流量。如果这个集合丢了，会不会破坏"不下载两次"？

## A
**不会。** 已发集合只是缓存，丢了顶多多发消息；真正的去重在主人的已见集合里，重复到达的 URL 仍会被主人拦住。

**含义。** 正确性只依赖主人的已见集合，已发集合只影响通信量。
