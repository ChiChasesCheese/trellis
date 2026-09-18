%% trellis:begin %%
# 定位读取位置：seek、按时间戳查找与重放（replay）
*消费者：从Kafka读取数据*

掌握用 seekToBeginning/seekToEnd、offsetsForTimes 与 seek() 把消费者跳到任意偏移量，用于重放历史、跳过积压或按时间点恢复。

**Requires:** [[domains/kafka/map/consumer.offset-commit|提交与偏移量管理]]

## Readings
- [[kafka-4-8-seek-and-replay|从特定偏移量位置读取记录：seek 与按时间戳定位]]

## Cards (4)
- [[kafka-consumer-offsetsfortimes-seek-mechanism]]
- [[kafka-consumer-seek-changes-poll-position-not-commit]]
- [[kafka-consumer-seek-use-cases]]
- [[kafka-consumer-seektobeginning-seektoend-purpose]]
%% trellis:end %%

## Notes
