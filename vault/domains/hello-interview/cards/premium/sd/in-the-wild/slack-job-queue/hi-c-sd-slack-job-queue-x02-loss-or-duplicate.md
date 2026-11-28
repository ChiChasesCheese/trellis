---
id: hi-c-sd-slack-job-queue-x02-loss-or-duplicate
node: sd.in-the-wild.slack-job-queue.exam
type: qa
step: 8
---
## Q
**Slack 作业队列 · 哪里会丢、哪里会重复**｜考点 · 必会

沿着"Web 应用 → Kafkagate → Kafka → JQRelay → Redis → worker"逐跳分析，哪些故障会让作业丢失，哪些会让作业重复？计费作业该怎么改？

## A
- **可能丢失：** Kafkagate 只等 leader 确认，leader 在复制前宕机，该作业丢失；开启非干净选举时，已确认的写入也可能丢。
- **可能重复：** JQRelay 写入 Redis 后、提交偏移量前崩溃，重启后同一批作业会再写一次（Redis 的有限去重能挡掉一部分）；worker 执行完但确认前崩溃，作业也会被再次执行。整体是至少一次。
- **计费作业的改法：** 生产者设置等待全部同步副本确认（`acks=all`）并关闭非干净选举，用牺牲延迟换取不丢；作业本身做成幂等——以业务唯一键（如订单号 + 周期）去重，重复执行不会重复计费。
- **思路：** 按作业的价值分级配置，不是全局一刀切；这也是 Slack 对"多数作业"选最低延迟的理由。
