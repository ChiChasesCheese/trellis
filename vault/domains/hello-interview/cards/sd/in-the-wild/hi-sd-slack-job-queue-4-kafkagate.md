---
id: hi-sd-slack-job-queue-4-kafkagate
node: sd.in-the-wild.slack-job-queue
type: qa
step: 4
---
## Q
**Kafkagate：入队路径**｜系统设计 · 业界案例

Slack 的入队网关 Kafkagate 做什么？它在持久性和延迟上做了什么取舍？

## A
**要点。** Kafkagate 是一个无状态的 Go 服务，对 Web 应用暴露普通的 HTTP POST（带主题、分区和任务内容），内部保持与 broker 的长连接，跟随分区领导者的变化，同步写入，调用方总会拿到明确的成功确认或错误。

**取舍。** 它只等分区领导者确认，不等副本复制。换来最低延迟，代价是 broker 在复制前宕机时有很小概率丢任务；Slack 判断对大多数任务这样合适。

**细节。** 入队的主机优先使用同可用区的 Kafkagate，必要时故障转移。这也去掉了连接扇出的入队那一半：Web 应用只连附近的网关，而不是连着五十个 Redis 集群。

**易错。** 答题时别只说「写 Kafka」：同步还是异步、等几个副本确认，都是该被问到的取舍点。
