---
id: hi-ov-slack-job-queue-2-options
node: sd.in-the-wild.slack-job-queue
type: qa
step: 2
tags: [通览]
---
## Q
**Slack 作业队列 · 关键决定**｜通览

Slack 作业队列里有哪些关键决定？各自为什么、代价是什么？

## A
**5 个决定。**
- **Kafka 放在 Redis 前面：** 积压存磁盘，受保留时间而非内存限制；Redis 满了就锁死；要同时运维两套队列式系统。
- **不用 Kafka 取代 Redis：** 保留 Redis 的去重、重试等既有语义，只做最小改动；重写应用会把可用性修复变成重构；Redis 仍是短队列和调度工作空间。
- **Kafkagate 只等 leader 确认：** 写 Kafka 时只等分区 leader；延迟最低；leader 在复制前宕机会丢少量作业。
- **JQRelay 限速排空，Consul 加锁：** 一个主题一个中继，写进 Redis 后才提交偏移量，限速值放在 Consul；积压时入队全速、排空可调；Redis 宕机时中继无限重试，作业可能重复。
- **双写加影子模式上线：** 新旧两条路同时写，中继先只读不写；真实流量走遍新组件而无用户影响；多一套对账和心跳监控。

**先后顺序。** 先保护入队路径，调度和 worker 扩容留到新路径跑稳之后。
