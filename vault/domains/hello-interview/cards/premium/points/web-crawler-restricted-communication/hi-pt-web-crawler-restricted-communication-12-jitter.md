---
id: hi-pt-web-crawler-restricted-communication-12-jitter
node: qb.sd.web-crawler-restricted-communication.points
type: qa
step: 12
---
## Q
**无中心网络爬虫 · 流量均衡**｜加分 · 出自：无中心网络爬虫 › 深入 7

要让任何单个节点对目标站点的流量都低且均衡，除了均分速率，还有什么做法？爬完之后页面在哪里？

## A
**做法。** 请求间隔加随机抖动，各节点速率相同。

**页面位置。** 爬完后页面仍分散在 10,000 台机器上，下游按 URL 指纹查位置即可，不需要汇总到一处。
