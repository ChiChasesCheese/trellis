---
id: hi-pt-web-crawler-design-7-dns-bottleneck
node: qb.sd.web-crawler-design.points
type: qa
step: 7
---
## Q
**网络爬虫 · DNS 瓶颈**｜出自：网络爬虫 › 深入 3

爬虫规模下 DNS 为什么常被忽略却可能成瓶颈？怎么缓解？

## A
**问题。** 早期爬虫线程有很大比例时间花在 DNS 解析上。
**做法。** 节点本地缓存，同一主机所有 URL 复用解析结果；必要时自建递归解析器或多个解析服务商轮询。
**对比。** 每主机每秒 1 次不妨碍总吞吐，因为同时爬数亿个不同主机，每个速率很低。
