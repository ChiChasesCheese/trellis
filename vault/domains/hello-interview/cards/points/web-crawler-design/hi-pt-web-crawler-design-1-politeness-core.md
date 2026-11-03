---
id: hi-pt-web-crawler-design-1-politeness-core
node: qb.sd.web-crawler-design.points
type: qa
step: 1
---
## Q
**网络爬虫 · 瓶颈是礼貌而不是计算**｜必会 · 出自：网络爬虫 › 需求

设计一个全网规模的爬虫，瓶颈在哪里？核心设计思想是什么？

## A
**要点。** 瓶颈不是计算而是礼貌：每个站点每秒只能被轻轻碰一下，而全网有上亿个站点。
**设计核心。** 按主机组织的前沿队列（URL frontier），让成千上万个站点并行、每个站点串行；再加不丢进度的流水线、URL 与内容两层去重、防止陷入爬虫陷阱。
