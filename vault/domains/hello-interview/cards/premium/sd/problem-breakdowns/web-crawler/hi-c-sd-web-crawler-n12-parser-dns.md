---
id: hi-c-sd-web-crawler-n12-parser-dns
node: sd.problem-breakdowns.web-crawler.notes
type: qa
step: 12
---
## Q
**网络爬虫 · 深入三：解析 worker 与 DNS 瓶颈**｜摘要 · 必会

解析 worker 怎样扩缩容？为什么 DNS 在这个规模下会成为瓶颈，怎么缓解？

## A
- **解析 worker：** 任务简单：从 blob 下载 HTML、提取文本、写回 blob。不必精确估算数量，按"后续处理队列"的积压长度自动伸缩，用 Lambda 或 ECS on Fargate 这类自动扩缩容的计算资源。
- **DNS 为什么是隐藏瓶颈：** curl 会自动解析，所以容易被忽略。但每秒数千请求、涉及数百万个不同域名时，每个新域名要经过多次 DNS 层级往返。早期爬虫研究（Mercator）发现，自建解析器之前，DNS 查询占了每个线程最多约 70% 的耗时。
- **加钱：** 第三方 DNS 服务商的限额通常可以花钱提高，时间紧时是个选项。
- **DNS 缓存：** 同一域名的所有 URL 共用一次解析结果。
- **多家服务商轮询：** 把负载分摊到多家，降低撞到限额的风险；简单而务实，跳出了"学院派"答案。
