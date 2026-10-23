---
id: hl-bq-q11-followups
node: behavioral.question-bank
type: qa
step: 24
---
## Q
"分布式存储"之后的追问：Kafka sink 的并行度怎么算？为什么 clone 和剪枝便宜？你运营过集群吗？
How does Kafka sink parallelism work? Why are clones and pruning cheap? Have you operated a cluster?

## A
- **Kafka sink 并行度**：**replicas × tasks.max**，**被分区数封顶**。
- **为什么便宜**：**不可变微分区 + 元数据指针**；clone 只复制元数据，剪枝靠元数据跳过分区。
- **运营过集群吗？** 没有；我**理解模型**，也会去学你们的。
