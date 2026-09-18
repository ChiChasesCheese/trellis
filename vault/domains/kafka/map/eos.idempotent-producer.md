%% trellis:begin %%
# 幂等生产者的工作原理与局限性
*精确一次语义（exactly-once semantics）*

理解幂等生产者依靠生产者ID与序列号去重的机制，以及它仅保证单个生产者会话内单分区幂等的局限。

**Requires:** [[domains/kafka/map/producer.idempotence-ordering|幂等生产者开关（enable.idempotence）与顺序保证]]

## Readings
- [[kafka-8-1-idempotent-producer|幂等生产者]]

## Cards (6)
- [[kafka-eos-idempotent-broker-failover-state-transfer]]
- [[kafka-eos-idempotent-limit-app-level-duplicate-send]]
- [[kafka-eos-idempotent-limit-multiple-producer-instances]]
- [[kafka-eos-idempotent-out-of-order-seq-error]]
- [[kafka-eos-idempotent-pid-sequence-dedup]]
- [[kafka-eos-idempotent-producer-restart-blindspot]]
%% trellis:end %%

## Notes
