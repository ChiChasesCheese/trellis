%% trellis:begin %%
# 幂等生产者开关（enable.idempotence）与顺序保证
*生产者：向Kafka写入数据*

理解开启幂等性如何消除重试导致的重复写入，并保障单分区内的消息顺序。

**Core** — part of the first pass through this subject.

**Unlocks:** [[domains/kafka/map/eos.idempotent-producer|幂等生产者的工作原理与局限性]]

## Readings
- [[kafka-3-4-producer-config|生产者关键配置：acks、批处理与幂等性]]

## Cards (5)
1. [[kafka-producer-idempotence-duplicate-scenario]]
2. [[kafka-producer-idempotence-sequence-number-mechanism]]
3. [[kafka-producer-idempotence-config-cloze]]
4. [[kafka-producer-idempotence-solves-ordering]]
5. [[kafka-producer-idempotence-exactly-once-relation]]
%% trellis:end %%

## Notes
