%% trellis:begin %%
# KRaft模式与ZooKeeper的移除
*集群内部机制：控制器、复制协议与存储*

理解Kafka 3.3+/4.0用基于Raft的KRaft控制器取代ZooKeeper后，元数据管理与控制器选举方式发生的根本变化。

## Readings
- [[kafka-6-2-controller-kraft|控制器的选举与职责，以及KRaft带来的变革]]

## Cards (5)
1. [[kafka-internals-kraft-motivation]]
2. [[kafka-internals-kraft-metadata-as-log]]
3. [[kafka-internals-kraft-active-standby-controller]]
4. [[kafka-internals-kraft-pull-metadata-fetch]]
5. [[kafka-internals-kraft-broker-fencing]]
%% trellis:end %%

## Notes
