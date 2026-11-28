---
id: hi-c-sd-web-crawler-n16-extras
node: sd.problem-breakdowns.web-crawler.notes
type: qa
step: 16
---
## Q
**网络爬虫 · 可以补充的深入话题**｜摘要 · 追问

除了容错、礼貌、规模，爬虫还有哪些值得补充的深入话题？各自怎么处理？

## A
- **动态内容：** 很多网站用 React、Angular 等框架，HTML 里没有正文，内容由 JavaScript 加载。要用无头浏览器（如 Puppeteer）渲染后再提取。
- **监控：** 用 Datadog、New Relic 之类监控爬虫和解析 worker 的表现，出问题告警。
- **大文件：** 先发 HTTP HEAD 请求看 `Content-Length`，超过阈值（如 10 MB）就跳过，不下载全文。
- **持续更新：** 如果不是一次性爬取（定期重训练、搜索引擎要保持新鲜），加一个 URL 调度器（URL Scheduler）：解析 worker 不再直接入队，而是把 URL 写进元数据库，由调度器按上次爬取时间、热度等逻辑决定何时入队。
- **优先级爬取：** 想优先爬热门域名，可用多个不同优先级的 SQS 队列，爬虫先读高优先级队列；Kafka 没有原生优先级消费，可用按优先级分开的主题近似。
