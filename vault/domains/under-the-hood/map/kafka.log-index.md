%% trellis:begin %%
# 分区日志：分段文件与稀疏索引
*Kafka*

每个分区是一串只追加的段文件；偏移量索引每隔约 4 KB 记一条，查找时二分索引再顺序扫描；时间索引同理。

**Core** — part of the first pass through this subject.

## Cards (3)
1. [[uth-kafka-log-index-1-sparse-index]]
2. [[uth-kafka-log-index-2-warm-section]]
3. [[uth-kafka-log-index-3-time-index]]
%% trellis:end %%

## Notes
