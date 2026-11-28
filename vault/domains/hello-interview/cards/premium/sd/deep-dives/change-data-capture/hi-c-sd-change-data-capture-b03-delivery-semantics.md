---
id: hi-c-sd-change-data-capture-b03-delivery-semantics
node: sd.deep-dives.change-data-capture.beyond
type: qa
step: 3
---
## Q
**变更数据捕获 · 拓展：CDC 的投递语义与细节**｜拓展 · 加分

面试官追问：CDC 的顺序、重复、删除、旧值分别怎样？有哪些坑？

## A
- **至少一次：** 连接器先把变更写出，再保存位置；崩溃后可能重发，所以消费者必须幂等。
- **顺序：** 只在同一个分区键内有序（通常是主键）；跨表、跨键没有全局顺序，不要依赖。
- **事务边界：** 一个事务改多行，下游看到的是一条条行变更，原子性不再保留；需要时要读事务标记或接受短暂中间态。
- **旧值：** Postgres 默认的复制标识（replica identity）只在更新和删除中带主键，要拿完整的 before 镜像，要对表设 `REPLICA IDENTITY FULL`，代价是日志更大。
- **删除：** 产生删除事件，消费者按主键删；Kafka 里常再跟一个墓碑（tombstone）供日志压缩清理。
- **表结构变化：** 加列、改类型会影响下游，要有 schema 注册和兼容规则。
