---
id: hl-bv-gap-dstore
node: behavioral.value-matrix
type: qa
step: 13
---
## Q
价值 6（分布式存储 / 计算集群）为什么算薄弱？被问到时的诚实说法是什么？

## A
现状：只有实习的**消费侧**（S11：Kafka 写入仓库）和**使用者视角**（S1 的 stream、S7 的不可变分区）；没有运营或设计过集群。

诚实说法："**I understand the model as a user; I haven't operated or designed one.**"（我以使用者的身份理解这套模型，没有运营或设计过。）

再补一句你确实知道的模型：不可变微分区加元数据（clone 与剪枝为什么便宜）、带 offset 的只追加 stream、Kafka sink 的并行度 = replicas × tasks.max 且受分区数封顶。
