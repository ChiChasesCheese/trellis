---
id: hi-sd-web-crawler-10-traps-extra
node: sd.problem-breakdowns.web-crawler
type: qa
step: 10
---
## Q
**爬虫陷阱与可补充的深入话题**｜系统设计 · 问题拆解

什么是爬虫陷阱（crawler trap）？怎样防？此外还可以补充哪些深入话题？

## A
**要点。** 陷阱是让爬虫永远爬不完的页面：页面反复链接到自己，或链接出大量新页面。办法是限制最大深度。深度指从种子 URL 起经过的链接跳数（种子为 0），不是 URL 路径的层数。在 URL 表加 depth 字段，每跟进一次链接加 1，超过阈值（15–20）就停止这条分支。

**补充话题。**
- 动态内容：JavaScript 渲染的页面要用无头浏览器（如 Puppeteer）。
- 监控：对爬虫和解析 worker 做健康监控和告警。
- 大文件：先发 HTTP HEAD 看 Content-Length，超过阈值（如 10 MB）就跳过。
- 持续更新：加一个 URL 调度器（URL Scheduler），按上次爬取时间、热度安排入队，而不是由解析 worker 直接入队。
- 优先级：多个不同优先级的 SQS 队列，爬虫先读高优先级队列；Kafka 则用按优先级分开的主题。
