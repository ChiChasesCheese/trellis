---
id: hi-c-sd-postgres-b03-failover-sync
node: sd.deep-dives.postgres.beyond
type: qa
step: 3
---
## Q
**PostgreSQL · 故障切换的真实风险与同步提交的粒度**｜拓展 · 加分

自动故障切换最怕什么？同步复制具体能配到什么程度？

## A
- **脑裂（split brain）：** 旧主其实没死，只是网络分区，新主已被提升，两边都在接受写入，数据分叉。必须有"围栏"（fencing）保证旧主不能再写，并通过分布式共识存储（如 etcd）保存"谁是主"的租约，这是 Patroni 之类工具的核心。
- **异步复制的数据丢失：** 提升时新主可能缺少旧主已确认的最后写入，丢失量就是复制延迟，这就是恢复点目标（RPO）。
- **同步粒度：** `synchronous_commit` 可设为 off、local、remote_write、on、remote_apply：off 连本地 WAL 落盘都不等；local 只等本地落盘、不等副本；remote_write 等副本收到并交给操作系统；on（默认，配置了同步副本时）等副本把 WAL 落盘；remote_apply 等副本回放完成，读副本能立刻看到。越往后越不丢数据，写延迟越高。
- **仲裁式同步：** `synchronous_standby_names` 可以写成"任意 1 个"，容忍单个同步副本故障而不阻塞写入。
- **复制槽的坑：** 一个停滞的副本会让主节点为它无限保留 WAL，最终撑满磁盘，需要监控。
- **2026 亮点：** PostgreSQL 17 起逻辑复制槽可以标成 failover 槽，备库开启 `sync_replication_slots`（默认关闭）同步这些槽，主备切换后 CDC 订阅者能从新主接着消费，不必全量重做；`pg_upgrade` 也能迁移逻辑槽（旧集群需是 17 或更高）。槽同步有滞后，切换后仍可能重复或回退，下游要按 LSN 或主键幂等。
