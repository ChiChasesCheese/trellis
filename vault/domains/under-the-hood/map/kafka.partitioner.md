%% trellis:begin %%
# 分区器：哈希与粘性分区
*Kafka*

有 key 时 murmur2 哈希取模；无 key 时粘性分区把一批消息先填满一个分区；增加分区会打乱 key 到分区的映射。

**Core** — part of the first pass through this subject.

## Cards (3)
1. [[uth-kafka-partitioner-1-key-hash]]
2. [[uth-kafka-partitioner-2-add-partitions]]
3. [[uth-kafka-partitioner-3-sticky-adaptive]]
%% trellis:end %%

## Notes
