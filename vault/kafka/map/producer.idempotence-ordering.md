%% trellis:begin %%
# 幂等生产者开关（enable.idempotence）与顺序保证
*生产者：向Kafka写入数据*

理解开启幂等性如何消除重试导致的重复写入，并保障单分区内的消息顺序。

**Unlocks:** [[eos.idempotent-producer|幂等生产者的工作原理与局限性]]

## Readings
- [[kafka-3-4-producer-config|生产者关键配置：acks、批处理与幂等性]]

## Cards (5)
- [[kafka-producer-idempotence-config-cloze]]
- [[kafka-producer-idempotence-duplicate-scenario]]
- [[kafka-producer-idempotence-exactly-once-relation]]
- [[kafka-producer-idempotence-sequence-number-mechanism]]
- [[kafka-producer-idempotence-solves-ordering]]
%% trellis:end %%

## Notes
