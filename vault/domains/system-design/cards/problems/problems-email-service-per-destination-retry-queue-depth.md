---
id: problems-email-service-per-destination-retry-queue-depth
node: problems.media.email-service
type: qa
step: 4
tags: [grown]
---
## Q
In an outbound email delivery design, a single global FIFO retry queue for all failed deliveries causes one slow or throttling destination domain to delay mail bound for every other domain behind it in the queue. What fixes this, and for a service sending 4.5 billion messages a day where 2% defer into retry with an average 6-hour dwell time, what does Little's Law say about the steady-state size of that retry state?

## A
Partitioning the retry queue per destination domain fixes it: each destination domain gets its own independent queue with its own backoff state, so one domain's temporary failure only delays mail to that domain, never mail queued behind it for healthy domains. By Little's Law (queue depth = arrival rate × average time in the queue), with 2% of 4.5 billion messages/day deferring (9×10^7/day, an arrival rate of about 1,042/second) and an average 6-hour (21,600-second) dwell time before final delivery or bounce, the steady-state retry queue holds on the order of 2.25×10^7 (22.5 million) messages at any given moment — a volume that requires the retry state to be durable, indexed storage rather than an in-memory list, since a single node can't hold it and a restart can't be allowed to lose it.

## Q zh
在一个出站邮件投递设计里，用单一全局 FIFO 队列处理全部失败投递，会导致一个响应缓慢或正在限流的目的域名，拖延排在它后面、发往其他健康域名的邮件。什么设计能解决这个问题？对于一个每天发送 45 亿封邮件、其中 2% 会延迟进入重试、平均在队列里停留 6 小时的服务来说，Little's Law 对这个重试状态的稳态规模给出了什么结论？

## A zh
按目的域名对重试队列分区能解决这个问题：每个目的域名拥有自己独立的队列和独立的退避状态，这样一个域名的临时故障只会延迟发往这个域名的邮件，绝不会连累排在它后面、发往健康域名的邮件。根据 Little's Law（队列深度 = 到达速率 × 平均停留时间），每天 45 亿封邮件中 2% 延迟进入重试（每天 9×10^7 条，到达速率约每秒 1,042 条），平均停留 6 小时（21,600 秒）才最终投递或退信，稳态下重试队列在任意时刻大约持有 2.25×10^7（2250 万）条消息——这个规模要求重试状态必须是持久化的、带索引的存储，而不是内存里的一个列表，因为单机内存放不下，也不能允许节点重启时丢失。
