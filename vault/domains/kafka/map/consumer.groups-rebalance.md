%% trellis:begin %%
# 消费者群组（consumer group）与再均衡（rebalance）
*消费者：从Kafka读取数据*

理解消费者群组如何分摊分区、再均衡的触发时机，以及再均衡监听器与群组固定成员（static membership）如何减少不必要的再均衡。

**Unlocks:** [[admin.consumer-group-ops|消费者群组管理与偏移量运维]]

## Readings
- [[kafka-4-1-consumer-groups|消费者与消费者群组]]
- [[kafka-4-7-rebalance-listener|再均衡监听器]]

## Cards (6)
- [[kafka-consumer-eager-vs-cooperative-rebalance]]
- [[kafka-consumer-group-partition-sharing]]
- [[kafka-consumer-heartbeat-session-timeout-death-detection]]
- [[kafka-consumer-multiple-groups-full-data]]
- [[kafka-consumer-rebalance-listener-commit-before-revoke]]
- [[kafka-consumer-static-membership-avoids-rebalance]]
%% trellis:end %%

## Notes
