---
id: bagu-link-job-scheduler-cron-history-1-map
node: links.job-scheduler-cron-history
type: qa
step: 1
---
## Q
**分布式任务调度器（含 cron 与一年执行历史） · 会被追问哪些八股**｜必会

设计分布式任务调度器（含 cron 与一年执行历史）时，面试官最可能从哪几步下钻到基础知识？每一步问什么，怎么答？

## A
**基本回答。** 难点是亿级任务里找到期的、节点会死而任务仍要执行且不重复。基础是：按时间排序的结构、带续期的锁和租约、幂等的状态更新、退避重试加死信。

**下钻路线。**
- 亿级任务里找到期的 → 按到期时间戳排序（ZSet 思路），多 worker 取任务要原子，[[b.redis.stream-delay-queue|Redis 做消息队列与延时任务]]
- 多个调度节点同时到点触发 → 抢锁，失败的直接放弃，不重试，[[a.distributed.lock-redis-setnx|用 Redis 实现分布式锁]]
- 长任务执行中防重复 → 带续期的租约，节点崩溃后过期才被接管，[[a.distributed.lock-watchdog|锁过期了业务没完]]
- 调度主节点切换会不会执行两次 → 锁在切换时可能丢，任务状态用条件更新做幂等，[[a.distributed.redlock|RedLock 与它受到的批评]]
- 调度器自己的高可用 → ZooKeeper 临时顺序节点选主，旧主 GC 醒来靠 fencing token 拦截，[[b.distributed.lock-zookeeper|用 ZooKeeper 实现分布式锁与 ZooKeeper 基础]]
- 任务反复失败 → 退避重试，超限进死信，毒任务不占满 worker，[[b.mq.dlq-retry|死信队列与重试设计]]
- 整点任务集体失败后重试 → 退避加抖动，调度器自己不能制造惊群，[[a.protect.retry|重试的原则与为什么不能无限重试]]
- 卡住的任务谁来发现 → 扫描中间状态，对账兜底，[[a.idem.selection-reconciliation|分布式事务选型、最终一致与对账]]

**业务场景。** 每晚 10 点按支付网络生成结算批次：两个调度节点同时触发会生成两份批次文件，所以批次号要做幂等键。
**系统设计。** [[links.payment-batch-processing|支付处理系统（授权冻结 + 每日批量结算）]]：每晚批处理要单领导者加围栏令牌，是这里的锁与租约的实例；[[links.notification-system-scale|通知系统（支持单发与群发，百万级每秒）]]：定时群发也靠到点触发，差别是触发量大，要分片并行。
