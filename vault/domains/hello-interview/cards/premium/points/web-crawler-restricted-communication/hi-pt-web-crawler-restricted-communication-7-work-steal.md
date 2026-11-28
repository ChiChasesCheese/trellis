---
id: hi-pt-web-crawler-restricted-communication-7-work-steal
node: qb.sd.web-crawler-restricted-communication.points
type: qa
step: 7
---
## Q
**无中心网络爬虫 · 空闲节点分担**｜必会 · 出自：无中心网络爬虫 › 深入 3

无中心爬虫稳态时，页面大小和响应速度不均，慢节点积压、快节点空闲。怎样让空闲机器分担，同时不破坏去重？

## A
**做法。** 空闲节点向随机邻居发 Steal，邻居从待爬队列尾部让出一批尚未开始的 URL。

**关键。** 去重权仍在主人手里（已见集合已记），只把下载委托出去；被委托者抽出的链接照常按哈希转发，页面存本机并告知主人位置。

**原则。** 去重（主人）与执行（任意节点）分离。
