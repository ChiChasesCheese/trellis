---
id: hi-pt-web-crawler-design-9-content-dedup
node: qb.sd.web-crawler-design.points
type: qa
step: 8
---
## Q
**网络爬虫 · 内容级去重**｜必会 · 出自：网络爬虫 › 深入 3

不同 URL 可能返回同一内容。精确重复和近似重复各用什么办法？

## A
**精确重复。** 内容哈希索引。
**近似重复。** 只差广告、时间戳的页面用 SimHash，汉明距离小于阈值视为重复，跳过解析与存储。
