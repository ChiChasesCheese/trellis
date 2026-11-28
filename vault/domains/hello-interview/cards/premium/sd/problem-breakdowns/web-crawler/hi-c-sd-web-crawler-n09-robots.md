---
id: hi-c-sd-web-crawler-n09-robots
node: sd.problem-breakdowns.web-crawler.notes
type: qa
step: 9
---
## Q
**网络爬虫 · 深入二：robots.txt 与 Crawl-delay**｜摘要 · 必会

什么是礼貌？爬虫怎样遵守 robots.txt 里的 Disallow 和 Crawl-delay，多个爬虫并行时怎样不冲突？

## A
- **礼貌（politeness）：** 不压垮站点、不占满它的带宽、遵守站点管理员的限制。
- **robots.txt：** `User-agent` 指明规则适用哪些爬虫，`Disallow` 禁止爬某些路径，`Crawl-delay` 要求两次请求间隔多少秒。`Crawl-delay` 不属于官方标准，Googlebot 就忽略它，但遵守是好的礼节。
- **步骤：**
  1. 对每个域名拉取 robots.txt，解析后存进元数据库（简化为只下载一次，实际可定期更新）；
  2. 从队列取到 URL，查该域名的规则；
  3. 被禁止就确认（ack）并丢弃；
  4. 允许则看 Crawl-delay，对比域名表记录的上次爬取时间；
  5. 间隔未到，用 `ChangeMessageVisibility` 延后；到了就爬并更新时间。
- **并发陷阱：** 两个爬虫同时取到同一域名的 URL，会读到同一个过期的"上次时间"。要用原子操作先拿域名锁，例如 Redis `SET key NX` 加与延迟等长的 TTL，拿不到就延后。
- **注意：** 已在途的消息要用 `ChangeMessageVisibility` 延后；`DelaySeconds` 只对新发送的消息有效。
