%% trellis:begin %%
# 提交与偏移量管理
*消费者：从Kafka读取数据*

掌握自动提交与手动同步/异步提交组合的权衡，以及如何提交特定偏移量。

**Requires:** [[domains/kafka/map/core.offsets|偏移量（offset）：仅追加日志中的位置]]

**Unlocks:** [[domains/kafka/map/consumer.seek-and-replay|定位读取位置：seek、按时间戳查找与重放（replay）]], [[domains/kafka/map/reliability.consumer-reliable|在可靠系统中配置消费者]]

## Readings
- [[kafka-4-6-commit-offsets|提交和偏移量]]

## Cards (6)
- [[kafka-consumer-auto-commit-duplicate-window]]
- [[kafka-consumer-commit-async-then-sync-on-shutdown]]
- [[kafka-consumer-commit-offset-duplicate-vs-loss]]
- [[kafka-consumer-commit-specific-offset-mid-batch]]
- [[kafka-consumer-commitsync-vs-commitasync]]
- [[kafka-consumer-offset-commit-meaning]]
%% trellis:end %%

## Notes
