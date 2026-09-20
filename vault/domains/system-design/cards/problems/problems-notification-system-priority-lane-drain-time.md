---
id: problems-notification-system-priority-lane-drain-time
node: problems.social.notification-system
type: qa
step: 1
tags: [grown]
---
## Q
In a multi-channel notification system, a marketing campaign enqueues 100 million notifications into a shared send queue whose worker pool processes 30,000 sends/second. Roughly how long does the queue take to drain, and why does this make a shared queue unacceptable for a system that also has to deliver OTP codes with P99 < 5 seconds?

## A
100,000,000 / 30,000 ≈ 3,333 seconds ≈ 55.6 minutes. If an OTP is enqueued right after the campaign batch on a FIFO shared queue, it can wait up to ~56 minutes behind the marketing traffic — far beyond the 5-second target, making the OTP feature effectively unusable. The fix is to give transactional and marketing notifications physically separate queues (separate topics/partitions and separate consumer pools), not just a priority field on one shared queue, so a marketing surge cannot starve transactional throughput.

## Q zh
在一个多渠道通知系统中，一次营销活动向共享发送队列入队 1 亿条通知，worker 池吞吐量为每秒 30,000 条。队列排空大约需要多久？这为什么使共享队列无法接受一个还要以 P99 < 5 秒送达 OTP 验证码的系统？

## A zh
100,000,000 / 30,000 ≈ 3,333 秒 ≈ 55.6 分钟。如果一条 OTP 恰好在营销批次之后入队 FIFO 共享队列，它最坏情况要等约 56 分钟才被处理——远超 5 秒目标，等于验证码功能完全不可用。解决办法是给事务性和营销通知物理隔离的队列（独立的 topic/partition 和独立的消费者池），而不只是在一条共享队列上加一个优先级字段，这样营销流量激增就不会拖垮事务性通知的吞吐。
