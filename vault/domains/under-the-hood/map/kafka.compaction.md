%% trellis:begin %%
# 日志压实：每个 key 只留最新值
*Kafka*

清理线程为脏段建一个 key 到最新偏移量的哈希表，再重写段文件；墓碑消息（value 为空）表示删除。

**Core** — part of the first pass through this subject.

## Cards (3)
1. [[uth-kafka-compaction-1-two-pass]]
2. [[uth-kafka-compaction-2-tombstone]]
3. [[uth-kafka-compaction-3-skimpy-probe]]
%% trellis:end %%

## Notes
