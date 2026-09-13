%% trellis:begin %%
# 分层存储（tiered storage, KIP-405）
*集群内部机制：控制器、复制协议与存储*

理解分层存储如何把冷数据下沉到低成本对象存储，从而把日志保留期与broker本地磁盘容量解耦。

## Readings
- [[kafka-6-5-physical-storage|物理存储：分层存储、分区分配、索引与压实]]

## Cards (5)
- [[kafka-internals-tiered-storage-decouple-storage-compute]]
- [[kafka-internals-tiered-storage-isolation-benchmark]]
- [[kafka-internals-tiered-storage-motivation]]
- [[kafka-internals-tiered-storage-read-path-choice]]
- [[kafka-internals-tiered-storage-two-layers]]
%% trellis:end %%

## Notes
