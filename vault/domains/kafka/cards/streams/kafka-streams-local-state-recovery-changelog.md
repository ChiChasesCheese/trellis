---
id: kafka-streams-local-state-recovery-changelog
node: streams.design-patterns
type: qa
step: 1
source: kafka-2e
---
## Q
Kafka Streams 应用把聚合状态保存在本地（比如内嵌的 RocksDB）里，如果这个应用实例发生崩溃、之后在同一台或另一台机器上重启，本地状态是怎么恢复回来的，而不会丢失？

## A
Streams 除了把状态写进本地的 RocksDB，还会把这个本地状态的每一次变更同步发送到一个 Kafka 主题（changelog 主题）里，比如把「IBM 当前最低价 167.19」这类变更记录下来；这个主题使用压缩日志（compacted topic，只保留每个键最新值的日志清理策略），所以不会随时间无限膨胀。当持有这份状态的实例崩溃后重新启动，或者这部分状态被重新分配给另一个实例时，新实例只需要把这个 changelog 主题从头到尾读一遍，重放里面的变更事件，就能重建出完全相同的本地状态，而不需要依赖那台原来机器上残留的任何数据。
