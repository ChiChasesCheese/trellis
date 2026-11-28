---
id: hi-pt-web-crawler-restricted-communication-11-politeness
node: qb.sd.web-crawler-restricted-communication.points
type: qa
step: 11
---
## Q
**无中心网络爬虫 · 礼貌与陷阱**｜追问 · 出自：无中心网络爬虫 › 深入 6

无中心爬虫要控制对目标站点的总请求速率，还要处理 robots.txt 和爬虫陷阱。没有中心限速器时怎么做？

## A
**速率。** 总上限按活跃节点数均分成每节点令牌桶；节点数变化时由 gossip 的成员数重算。

**robots.txt。** 每个节点本地读取。

**陷阱。** 无限日历之类靠 URL 深度、长度上限和页面内容指纹防。
