%% trellis:begin %%
# 副本、首领/追随者与同步副本集合（ISR）
*核心架构：主题、分区与副本模型*

掌握分区副本的首领-追随者模型，以及ISR如何界定哪些副本被视为已同步。

**Core** — part of the first pass through this subject.

**Unlocks:** [[domains/kafka/map/producer.acks-durability|acks与生产端持久性保证]], [[domains/kafka/map/internals.replication-protocol|复制协议：首领/追随者同步与副本滞后]], [[domains/kafka/map/reliability.broker-config|broker层可靠性配置]]

## Readings
- [[kafka-6-3-replication-protocol|复制协议：首领、跟随者与ISR]]

## Cards (5)
1. [[kafka-core-leader-follower-roles]]
2. [[kafka-core-isr-definition]]
3. [[kafka-core-isr-leader-election-eligibility]]
4. [[kafka-core-preferred-leader-rebalance]]
5. [[kafka-core-follower-reads-latency-tradeoff]]
%% trellis:end %%

## Notes
