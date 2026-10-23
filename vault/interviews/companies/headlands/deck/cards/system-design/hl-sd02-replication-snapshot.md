---
id: hl-sd02-replication-snapshot
node: system-design.sd02-job-scheduler
type: qa
step: 21
---
## Q
调度器怎么复制日志、做快照和恢复？选主用什么？热备有什么好处？

## A
- **复制**：leader → follower 顺序流式复制日志（概念上与 Raft 的 AppendEntries 同构），3 副本取 2 确认即提交。用 Raft / ZooKeeper 一类外部组件管理**选主与成员**，数据路径用自己的日志流以获得吞吐（Aeron Cluster 是 Raft + 复制状态机的 Java 实现，概念对应）；
- **快照**：每隔 N 分钟（或日志段滚动时）对内存状态做一致性快照（单写线程在 tick 间隙写出「当前日志位置 + 全部活动任务」），之后旧日志段可删除；
- **恢复** = 读最新快照 → 重放其后的日志 → 与崩溃前相同的状态；
- **热备**：follower 持续重放日志，状态始终近乎最新，故障切换不需要从快照冷启动。
