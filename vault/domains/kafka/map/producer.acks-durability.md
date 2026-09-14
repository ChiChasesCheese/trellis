%% trellis:begin %%
# acks与生产端持久性保证
*生产者：向Kafka写入数据*

理解acks=0/1/all如何决定消息在被确认前需要写入多少副本，以及由此带来的持久性保证差异。

**Requires:** [[core.replication-isr|副本、首领/追随者与同步副本集合（ISR）]]

**Unlocks:** [[reliability.producer-reliable|在可靠系统中配置生产者]]

## Readings
- [[kafka-3-4-producer-config|生产者关键配置：acks、批处理与幂等性]]

## Cards (5)
- [[kafka-producer-acks-0-fire-and-forget-risk]]
- [[kafka-producer-acks-1-leader-crash-risk]]
- [[kafka-producer-acks-all-isr-safety]]
- [[kafka-producer-acks-end-to-end-latency-same]]
- [[kafka-producer-acks-speed-vs-durability-tradeoff]]
%% trellis:end %%

## Notes
