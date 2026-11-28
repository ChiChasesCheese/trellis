---
id: hi-c-sd-flink-b01-backends-modern
node: sd.deep-dives.flink.beyond
type: qa
step: 1
---
## Q
**Flink · 状态后端的现状、增量检查点与保存点**｜拓展 · 加分

现在 Flink 的状态后端实际有哪几种？增量检查点和保存点（savepoint）解决什么？

## A
- **现状：** 新版本里只剩两类：基于堆内存的哈希表后端（HashMapStateBackend）和 RocksDB 后端（EmbeddedRocksDBStateBackend）。早期的"内存后端"与"文件系统后端"其实是同一种堆内存状态，只是检查点存放的位置不同。检查点存储（放 S3、HDFS 等）与状态后端是分开配置的。
- **增量检查点：** RocksDB 后端只上传自上次检查点以来变化的文件，而不是整份状态，状态大时检查点时间和网络开销大大下降。
- **保存点（savepoint）：** 由人手动触发的、可长期保存的一致快照，用于升级作业代码、改并行度、迁移集群；检查点则是系统自动创建、主要服务于故障恢复。
- **重新伸缩：** 状态按键组（key group）切分，最大并行度决定键组数量；重新设置并行度时只是把键组重新分配给实例，所以最大并行度要在一开始设够。
