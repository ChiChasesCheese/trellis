%% trellis:begin %%
# Kafka

分区日志、稀疏索引、零拷贝、分区器、日志压实、ISR、时间轮、消费者组分配。

## Topics
- [[domains/under-the-hood/map/kafka.log-index|分区日志：分段文件与稀疏索引]]
- [[domains/under-the-hood/map/kafka.zero-copy|页缓存、零拷贝与批量]]
- [[domains/under-the-hood/map/kafka.partitioner|分区器：哈希与粘性分区]]
- [[domains/under-the-hood/map/kafka.compaction|日志压实：每个 key 只留最新值]]
- [[domains/under-the-hood/map/kafka.replication|副本、ISR 与高水位]]
- [[domains/under-the-hood/map/kafka.timing-wheel|延迟操作：分层时间轮]]
- [[domains/under-the-hood/map/kafka.consumer-group|消费者组：位点与分区分配]]
%% trellis:end %%

## Notes
