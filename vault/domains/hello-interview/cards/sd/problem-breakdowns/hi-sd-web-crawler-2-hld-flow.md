---
id: hi-sd-web-crawler-2-hld-flow
node: sd.problem-breakdowns.web-crawler.exam
type: qa
step: 2
---
## Q
**爬虫的接口与高层设计**｜系统设计 · 问题拆解

这个爬虫没有用户界面。它的系统接口、数据流和最初的高层设计包含哪些组件？

## A
**要点。** 接口：输入种子 URL，输出网页文本。数据流：从 frontier 取 URL → DNS 解析 → 拉取 HTML → 提取文本 → 存文本 → 抽出链接加回 frontier → 重复，直到爬完。

**组件。**
- Frontier 队列：待爬 URL 队列，可用 Kafka、Redis 或 SQS，稍后再选型。
- Crawler：拉取页面、提取文本和新链接。
- DNS：域名解析，后面有缓存和限流的话题。
- 外部网页服务器。
- S3 文本存储：便宜、可扩展、持久的 blob 存储。

**易错。** 先从最简版本搭起，再按非功能需求逐条改进。顺带问清种子 URL 是否已提供；若没有，可从搜索引擎、新闻站、社交平台、网站目录入手。
