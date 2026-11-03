---
id: hi-sd-web-crawler-5-politeness-robots
node: sd.problem-breakdowns.web-crawler.exam
type: qa
step: 5
---
## Q
**robots.txt 与礼貌**｜系统设计 · 问题拆解

什么是礼貌（politeness）？爬虫怎样遵守 robots.txt 里的 Disallow 和 Crawl-delay？

## A
**要点。** 礼貌指不干扰站点正常运行：不压垮服务器、不占满带宽、遵守站点规则。robots.txt 里的 `User-agent` 指明规则适用于哪些爬虫，`Disallow` 禁止爬取某些路径，`Crawl-delay` 要求两次请求间隔多少秒。

**步骤。**
1. 对每个域名拉取 robots.txt，解析后存入元数据库（简化为只下载一次）。
2. 从队列取到 URL，查该域名的规则。
3. 被 Disallow：直接确认（ack）并丢弃。
4. 允许：看 Crawl-delay，对比域名表里记录的上次爬取时间。
5. 未到间隔：用 ChangeMessageVisibility 延后再处理；到了间隔就爬取并更新时间。

**易错。** 多个爬虫可能同时取到同一域名的 URL，读到同一个过期的上次时间。所以用原子操作（如 Redis 的 `SET NX` 加与延迟相同的 TTL）先拿域名锁，拿不到就延后。已经在途（in-flight）的消息要用 ChangeMessageVisibility 延后，DelaySeconds 只对新发送的消息有效。Crawl-delay 不属于官方标准，Googlebot 忽略它，但遵守它是礼貌。
