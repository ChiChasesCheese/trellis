---
id: nr-amz-s11-relp
node: amazon.s11
type: qa
step: 4
---
## Q
【实习期：Kafka 事件流 · Spring · Spark（广度补充）】换成别的 LP 问时，强调哪一段？

## A
- **Learn and Be Curious**：坏消息返回 NULL 的 converter、并行度模型；别声称运维过 Kafka 集群 / K8s，只有部署形态经验
- **Dive Deep**："Parallelism is replicas times tasks, capped by partitions."；幂等的三道防线
- **Insist on the Highest Standards**："One bad message must not poison the pipeline."：poison-message 处理
- **Deliver Results**："Three deliverables in one summer internship."：CDC 扩展、审计日志、Spark 校验；无数字别编
