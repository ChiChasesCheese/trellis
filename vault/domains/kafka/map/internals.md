%% trellis:begin %%
# 集群内部机制：控制器、复制协议与存储

深入broker内部：控制器职责、复制协议、请求处理路径，以及日志的物理存储、索引与压实机制。

## Topics
- [[domains/kafka/map/internals.controller|控制器（controller）的角色与选举]]
- [[domains/kafka/map/internals.replication-protocol|复制协议：首领/追随者同步与副本滞后]]
- [[domains/kafka/map/internals.request-handling|broker如何处理生产请求与获取请求]]
- [[domains/kafka/map/internals.storage-segments|物理存储：分区分配与日志片段（log segment）]]
- [[domains/kafka/map/internals.indexes|索引：偏移量索引与时间索引]]
- [[domains/kafka/map/internals.compaction|日志压实（log compaction）]]
- [[domains/kafka/map/internals.kraft-mode|KRaft模式与ZooKeeper的移除]]
- [[domains/kafka/map/internals.tiered-storage|分层存储（tiered storage, KIP-405）]]
%% trellis:end %%

## Notes
