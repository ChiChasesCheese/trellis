---
id: hl-bq-q11-dstore
node: behavioral.question-bank
type: qa
step: 23
---
## Q
你做过分布式存储或计算集群吗？（≤ 45 秒）
Have you worked on distributed storage or a compute farm?

## A
- **Consumer side of a scaled system**：Kafka sink 写入仓库，**每个 topic 一个部署**，并行度 = **replicas × tasks.max**，**被分区数封顶**。
- **Storage model as a user**：**不可变微分区 + 元数据**（所以 clone 便宜、剪枝有效）；**带 offset 的只追加 stream**。
- **Boundary**："I **haven't operated** a cluster or **designed** a storage engine; I **understand the model** and I'd learn yours."
