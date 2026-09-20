%% trellis:begin %%
# 分层存储（tiered storage, KIP-405）
*集群内部机制：控制器、复制协议与存储*

理解分层存储如何把冷数据下沉到低成本对象存储，从而把日志保留期与broker本地磁盘容量解耦。

## Readings
- [[kafka-6-5-physical-storage|物理存储：分层存储、分区分配、索引与压实]]

## Cards (5)
1. [[kafka-internals-tiered-storage-motivation]]
2. [[kafka-internals-tiered-storage-two-layers]]
3. [[kafka-internals-tiered-storage-decouple-storage-compute]]
4. [[kafka-internals-tiered-storage-read-path-choice]]
5. [[kafka-internals-tiered-storage-isolation-benchmark]]
%% trellis:end %%

## Notes
