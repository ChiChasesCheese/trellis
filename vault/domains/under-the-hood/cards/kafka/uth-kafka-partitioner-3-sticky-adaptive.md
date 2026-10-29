---
id: uth-kafka-partitioner-3-sticky-adaptive
node: kafka.partitioner
type: qa
step: 3
---
## Q
**无 key：粘性分区与加权随机**｜Kafka · 4.0

没有 key 的消息，生产者怎么挑分区？为什么不一条换一个分区地轮流（round-robin）？

## A
**结构。** 粘性分区（sticky）：一直写同一个分区，累计写满 `batch.size` 字节才换。3.3 起默认带自适应：换分区时按各分区待发队列的长短加权随机，队列短的更容易被选中。

**细节。**

- 权重存成累计频次表（`cumulativeFrequencyTable`）：随机数落在哪一段，用 `Arrays.binarySearch` 找到对应分区。
- `partitioner.adaptive.partitioning.enable` 默认 `true`。

**为什么。** 轮流写把连续消息拆散到所有分区，批次又小又多，请求多、排队多、延迟高；粘性让批次尽量写满，自适应再把更多消息交给队列短（响应快）的 broker。

**对应 LeetCode：** LC 528 按权重随机选择
