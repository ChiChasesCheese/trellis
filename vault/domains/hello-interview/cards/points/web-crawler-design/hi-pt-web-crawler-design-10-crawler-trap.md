---
id: hi-pt-web-crawler-design-10-crawler-trap
node: qb.sd.web-crawler-design.points
type: qa
step: 10
---
## Q
**网络爬虫 · 爬虫陷阱**｜出自：网络爬虫 › 深入 5

日历页面无限翻页、会话 ID 嵌入 URL、动态生成无限层级链接，怎么防？

## A
**防线。** 最大深度（从种子算起的链接跳数，15 到 20）、URL 长度上限、单主机页数上限、查询参数个数上限，以及按路径模式的重复率检测。
