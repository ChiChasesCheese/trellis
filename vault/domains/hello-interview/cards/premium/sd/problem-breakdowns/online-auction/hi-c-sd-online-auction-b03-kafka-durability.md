---
id: hi-c-sd-online-auction-b03-kafka-durability
node: sd.problem-breakdowns.online-auction.beyond
type: qa
step: 3
---
## Q
**在线拍卖 · 拓展：Kafka 里"不丢出价"的具体配置**｜拓展 · 加分

"出价写入 Kafka 就不会丢"，具体要怎么配置才成立？Kafka 确认为什么不等于出价被接受？

## A
- **生产者：** `acks=all`，等所有同步副本（ISR）确认才算成功；开幂等生产者（`enable.idempotence=true`），重试不会产生重复消息。
- **主题：** 复制因子 3，`min.insync.replicas=2`：同步副本少于 2 个时拒绝写入，宁可写失败让客户端重试，也不在只有一份副本时假装成功。
- **消费者：** 关闭自动提交位点，入库成功后再手动提交，崩溃只会重复处理（至少一次），配合幂等入库。
- **Kafka 确认的含义：** 只说明"收到并持久了"，不说明出价被接受（可能被拒绝：价格不够）。所以接口应当返回 202 和 bidId，结果经 SSE 推给用户，或由客户端凭 bidId 查询。
- **取舍：** 同步等 ISR 增加几毫秒延迟，换来在单个 Broker 故障时不丢。
- **模式。** 先写日志：把请求先持久化为一条有序日志，处理可重放，是"命令队列"的核心。
