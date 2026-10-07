# sd01 · Rubric

| 维度 | strong | ok | weak |
|---|---|---|---|
| 量化 | 先算：50k ev/s × 1 KB = 50 MB/s、4.32 B events/day ≈ 4.3 TB/day；每个事件 1 次 history 查询 = 5 万 QPS 打 Postgres；一个租户 40% = 2 万 ev/s 进同一 partition | 给了吞吐但没推到每个组件 | 不算数，直接画新架构 |
| 找第一个瓶颈 | 指出**按事件查 Postgres（history + brute_force 的 count）**与**把原始事件写进 OLTP 主库**最先崩；按 tenant_id 分区让大租户成为热分区；每事件两次同步 HTTP | 说"DB 是瓶颈"但不说哪类查询 | "加 pod" |
| 写路径 | 原始事件不进 Postgres：Kafka → 对象存储（S3/Parquet，按 tenant/day 分区）+ 搜索索引（OpenSearch，30 天 ILM）；Postgres 只存告警与有界状态；告警按去重键 upsert（幂等） | 提到冷热分层但没说告警幂等 | 给 Postgres 加 IOPS / 分库分表了事 |
| 状态与 enrichment | 分区键改为 hash(tenant_id, user)：同一用户的事件落同一 consumer，**窗口与历史状态放 consumer 本地/键控状态**（内存 + 定期快照，或 Redis 按 key 分片），按 user 有序；geo-ip 用进程内 mmdb、威胁情报进程内集合定期刷新——去掉每事件网络调用 | 加 Redis 缓存 history | 每事件仍查 DB |
| 读路径 | 告警列表：`(tenant_id, status, score DESC, id)` 复合索引 + keyset 分页替代 OFFSET；score 写时计算；只读副本承接 API；事件检索走 OpenSearch；计数类查询缓存 | 加只读副本 | 只说缓存 |
| 扩容的极限 | 说出：consumer 数 ≤ partition 数；热 key（大租户里的服务账号）还会热——拆 key 或 per-key 采样/预聚合；下游（OpenSearch 索引速率、S3 小文件）也有上限；按租户配额防 noisy neighbor | 提到 partition 上限 | 无 |
| 失败与正确性 | at-least-once + 幂等告警；consumer 重启从 offset 回放，状态快照 + 回放窗口；DLQ + 毒消息；lag 与端到端延迟 SLO 告警；迁移路径（双写、影子对比、分租户切流） | 提到 DLQ | 无 |
| 沟通 | 先现状瓶颈再方案；每个改动说"解决哪个数" | | 一次性画终态图 |
