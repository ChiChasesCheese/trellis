---
id: hi-sd-web-crawler-8-dns-parser
node: sd.problem-breakdowns.web-crawler.exam
type: qa
step: 8
---
## Q
**DNS 瓶颈与解析 worker**｜系统设计 · 问题拆解

爬虫规模到每秒数千页、涉及数百万个不同域名时，为什么 DNS 会成为瓶颈？怎样缓解？解析 worker 要怎样扩缩容？

## A
**要点。** 每个新域名的查询要经过多次 DNS 层级往返。早期爬虫研究（Mercator）发现，在自建解析器之前，DNS 查询占了每个线程最多约 70% 的耗时。

**取舍。**
- 加钱：向第三方 DNS 提高限额。
- DNS 缓存：同一域名的 URL 共用一次解析结果。
- 多家 DNS 服务商轮询：分摊负载，降低触及限额的风险；这是一个很务实的想法。

**解析 worker。** 它们只做下载 HTML、提取文本、写回 blob，任务简单。不必精确估算数量，只要按「后续处理队列」的积压长度自动伸缩，用 Lambda 或 ECS on Fargate 这类自动扩缩容计算即可。

**易错。** curl 会自动做 DNS，容易让人忽略它；只有规模上去才会暴露。
