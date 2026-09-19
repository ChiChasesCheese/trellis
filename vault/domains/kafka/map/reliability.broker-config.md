%% trellis:begin %%
# broker层可靠性配置
*可靠的数据传递*

掌握复制系数、不彻底的首领选举（unclean leader election）与最少同步副本（min.insync.replicas）如何共同决定可用性与数据丢失风险之间的取舍。

**Requires:** [[domains/kafka/map/core.replication-isr|副本、首领/追随者与同步副本集合（ISR）]]

## Readings
- [[kafka-7-3-broker-reliability-config|broker配置：复制系数、不彻底首领选举与最少同步副本]]

## Cards (6)
1. [[kafka-reliability-replication-factor-tradeoffs]]
2. [[kafka-reliability-rack-awareness]]
3. [[kafka-reliability-min-insync-replicas]]
4. [[kafka-reliability-unclean-leader-election-tradeoff]]
5. [[kafka-reliability-flush-to-disk-vs-replication]]
6. [[kafka-reliability-lag-timeouts-tuning]]
%% trellis:end %%

## Notes
