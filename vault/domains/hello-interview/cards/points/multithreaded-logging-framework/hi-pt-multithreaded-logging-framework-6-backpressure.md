---
id: hi-pt-multithreaded-logging-framework-6-backpressure
node: qb.lld.multithreaded-logging-framework.points
type: qa
step: 6
---
## Q
**多线程日志框架 · 背压与满队列策略**｜出自：多线程日志框架 › 深入 1

日志洪峰时生产速度远大于磁盘写速度，队列该怎么设计？满了的时候有哪些处理选项，默认选哪个？

## A
**问题。** 无界队列会让内存无限增长直至 OOM，所以用有界队列。
**选项。** 满了阻塞调用方（不丢但可能拖慢业务）；丢弃新日志；丢最旧的；按级别区分，丢调试日志留错误日志。
**选择。** 默认阻塞，因为不丢日志是日志框架的基本承诺；延迟极敏感的路径可配置为丢弃，并记录丢弃计数。
