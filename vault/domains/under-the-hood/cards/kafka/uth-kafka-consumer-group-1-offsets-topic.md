---
id: uth-kafka-consumer-group-1-offsets-topic
node: kafka.consumer-group
type: qa
step: 1
---
## Q
**位点存在哪：__consumer_offsets**｜Kafka · 4.0

消费者提交的位点（offset）存在哪里？一个消费者组的位点由哪台 broker 负责？

## A
**结构。** 存在内部主题 `__consumer_offsets`：key 是（组、主题、分区），value 是位点。这个主题开了压实，只留每个 key 的最新值。

**细节。**

- 默认 50 个分区（`offsets.topic.num.partitions`），副本因子 3。
- 组到分区：`abs(groupId.hashCode()) % 50`；该分区 leader 所在的 broker 就是这个组的协调者（coordinator）。
- 位点默认保留 7 天（`offsets.retention.minutes`），从组变空开始计时。

**为什么。** 位点本质是一张 (组, 主题, 分区) → 位点 的映射，用压实日志存，不必再引入存储系统；按组名哈希分片，协调工作均匀分到各台 broker。

**对应 LeetCode：** LC 706 设计哈希映射 · LC 705 设计哈希集合
