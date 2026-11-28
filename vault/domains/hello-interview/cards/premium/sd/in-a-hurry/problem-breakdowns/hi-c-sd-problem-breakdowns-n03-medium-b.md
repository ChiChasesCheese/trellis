---
id: hi-c-sd-problem-breakdowns-n03-medium-b
node: sd.in-a-hurry.problem-breakdowns.notes
type: qa
step: 3
---
## Q
**常见题目拆解 · 中等题下半（9 道）**｜摘要 · 必会

中等难度里 Distributed Cache、Rate Limiter、Online Auction、YouTube、Job Scheduler、FB Live Comments、News Aggregator、Price Tracking Service、Notification System 各自的考点是什么？

## A
- **Distributed Cache：** 分片（一致性哈希）、复制、淘汰策略、热点键、故障转移。基础设施题，重在数据结构与分布式细节。
- **Rate Limiter：** 令牌桶 / 滑动窗口等算法、在分布式环境里如何共享计数（Redis 原子操作）、限流位置（网关 / 服务内）。
- **Online Auction：** 同一商品的出价竞争、保证最高价的一致性、把新出价实时推给围观者。
- **YouTube：** 大视频上传、转码流水线、自适应码率播放、CDN 分发。
- **Job Scheduler：** 按时间触发任务、至少一次执行、任务分片给 worker、故障恢复。
- **FB Live Comments：** 一路直播的评论扇出给海量观众，实时推送与热点。
- **News Aggregator：** 汇集多个来源、去重、排序、新鲜度、分页。
- **Price Tracking Service：** 定期采集价格、检测变化、通知订阅者。
- **Notification System：** 多渠道（推送 / 邮件 / 短信）、重试、优先级、限速与去重。
