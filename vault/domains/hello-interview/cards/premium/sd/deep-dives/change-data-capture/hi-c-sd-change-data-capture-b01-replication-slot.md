---
id: hi-c-sd-change-data-capture-b01-replication-slot
node: sd.deep-dives.change-data-capture.beyond
type: qa
step: 1
---
## Q
**变更数据捕获 · 拓展：连接器停摆会撑爆数据库磁盘**｜拓展 · 加分

Postgres 的 CDC 连接器挂了两天没人发现，线上库磁盘告警。为什么？怎么预防？

## A
- **原因：** Postgres 的逻辑解码用复制槽（replication slot）记录消费者读到哪里；只要槽还没被消费，Postgres 就必须保留对应的 WAL，不能回收。连接器停了，WAL 一直堆积，直到磁盘写满。
- **后果：** 磁盘满了会让主库本身停止写入，从下游的问题变成线上事故。
- **预防：**
  - 监控复制槽落后的字节数和槽是否活跃，告警；
  - Postgres 13 起可设 `max_slot_wal_keep_size` 给槽设上限，超了就废弃该槽（代价是下游要重做快照）；
  - 不再使用的连接器，要删除它的槽。
- **2026 亮点：** `max_slot_wal_keep_size` 默认 -1，即槽可以无限保留 WAL，必须显式设成磁盘预算内的上限；PostgreSQL 18 再加 `idle_replication_slot_timeout`，空闲超时的槽会被作废（默认 0 即关闭，只能在配置文件里设）。两道保险的代价相同：槽被作废后下游必须重做全量快照，所以仍要监控 `pg_replication_slots` 的保留量。
- **MySQL 对比：** binlog 有保留期，过期会被清掉，连接器落后太久会找不到位置，只能重新快照。
