---
id: hi-c-sd-web-crawler-x01-receive-count
node: sd.problem-breakdowns.web-crawler.exam
type: qa
step: 12
---
## Q
**网络爬虫 · 预测失败：礼貌延后把正常 URL 送进死信队列**｜考点 · 必会

某大站的 5000 个 URL 同时在 SQS 队列里，该站 Crawl-delay 为 10 秒。爬虫每次取到它的 URL，发现没到间隔，就用 `ChangeMessageVisibility` 延后；队列的 `maxReceiveCount` 为 5。会发生什么？怎么改？

## A
- **后果：** 每次 `ReceiveMessage` 都使 `ApproximateReceiveCount` 加一。同一域名的 URL 每 10 秒只放行一个，其余 4999 个反复被取到、延后，不到几分钟就超过 5 次，被自动送进死信队列，实际上并没有失败过，这些网页从此丢失。
- **根因：** 把"礼貌等待"和"拉取失败"混在同一个计数器里，该计数器只该代表失败。
- **改一，按域名分队列或分区：** 每个域名（或哈希到某个队列的一组域名）一个逻辑队列，只有轮到该域名时才取，等待不再消耗接收次数。
- **改二，用调度表代替延后：** 域名表里存 `next_allowed_time`，调度器到时间才把 URL 放进可处理队列。
- **改三，失败次数自己记：** 在元数据库里记录真正的拉取失败次数，DLQ 只靠它判断，不依赖接收次数。
- **要点：** 复用基础设施的计数时，要确认它数的是不是你想数的东西。
