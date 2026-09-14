# 模型答案：PB 级数据库间同步

> 取材：Reddit 一手（IC2，不许澄清需求）；Debezium / Netflix DBLog 的快照 + 增量拼接思路；Snowflake Openflow CDC、Snowpipe Streaming offset token（`../../../01-company-brief.md` §2.6、§2.11）。

## 0. 假设声明 + 不变量（开场 2 分钟，因为不许澄清）

**声明的假设**：源端是带变更日志的事务库（MySQL binlog / Postgres WAL，每条变更有单调 LSN）；目标端是列式分析库；目标延迟分钟级；源端数万张表、最大单表几百 TB、最热表 10⁵ 行/秒变更；同步单向。

**不变量**：
1. **源端不停写、不被拖慢**：读取只走副本或存储快照，全量搬运限速。
2. **断点可续**：任何组件崩溃后从最后持久化的位点继续，不重搬已完成的块。
3. **收敛**：对每张表，存在一个 LSN，使目标端内容等于源端在该 LSN 的快照；apply 幂等且乱序安全。
4. **可验证**：随时能回答"这张表一不一样、落后多少"。

**不做**：目标端不保证跨表事务的实时原子可见；不做双向同步；不承诺秒级延迟。

## 1. API 契约

控制面：
- `RegisterTable(source_table, target_table, pk, options{max_rate, chunk_size})` → 进入 `backfill`
- `GetTableStatus(table)` → `{phase, snapshot_lsn, applied_lsn, lag_seconds, backfill_progress, last_verify}`
- `Verify(table, pk_range?)` → 分块 checksum 结果
- `Resync(table)` → 重新快照（位点落后超过日志保留时）

变更事件（数据面内部）：
```
ChangeEvent { table, pk, op: INSERT|UPDATE|DELETE, after: row|null, commit_lsn, txn_id, schema_version }
```

## 2. 数据模型

- `table_sync_state(table PK, phase, snapshot_lsn, applied_lsn, backfill_cursor, schema_version, updated_at)` —— 唯一的有状态控制数据，放强一致存储。
- `backfill_chunks(table, chunk_id, pk_lo, pk_hi, status, row_count, checksum)` —— 每块独立完成、可重做。
- 变更流：按 `(table, hash(pk))` 分区的持久日志；每分区内按 LSN 有序。
- 目标表每行带 `_last_lsn`、`_deleted`（软删）隐藏列。

## 3. 核心流程

**接入一张表（快照 + 增量拼接）**：
1. 记录 `snapshot_lsn = source.current_lsn()`，同时 CDC 读取器开始把该表 ≥ snapshot_lsn 的变更写入变更流（先缓冲，不 apply）。
2. 从副本上按 pk 范围切块（每块数百 MB），并行搬运；每块写目标的 staging，完成后记 checksum 并把 `backfill_chunks.status=done`。
3. 全量完成 → 切 `phase=catchup`：apply worker 从 snapshot_lsn 起回放缓冲的变更，`MERGE ON pk WHEN incoming.commit_lsn > target._last_lsn`。全量期间被改过的行，快照里是旧值，回放后被新值覆盖；快照里读到的比 snapshot_lsn 更新的值（副本读的非一致点），也会因 LSN 比较而不被旧事件回滚。
4. 积压追平 → `phase=streaming`，持续 apply；`applied_lsn` 定期持久化。

**删除**：DELETE 事件 → `_deleted=true, _last_lsn=lsn`；定期物理清理。

**Schema 演进**：事件带 `schema_version`；加列 → 目标先加列（可空）再放行新版本事件；改类型 → 影子列 + 回填 + 切换；拆表 → 作为新表注册。

## 4. 失败模式与规模

| 失败 | 处理 |
|---|---|
| 全量搬运器崩溃 | 从 `status != done` 的块继续；块幂等（先写 staging 再原子替换） |
| apply worker 崩溃 | 从 `applied_lsn` 重放；MERGE 按 LSN 幂等，重复 apply 无害 |
| 变更流乱序 / 重复 | 分区内有序；跨分区只影响不同 pk；LSN 比较挡住旧事件 |
| 源端变更日志保留期不够（落后太久） | 检测 `applied_lsn < oldest_available_lsn` → 该表 `Resync` |
| 热表 10⁵ 行/秒 | 按 pk 哈希分区并行 apply；目标端微批（秒级攒批写 100–250 MB 文件）而非逐行 |
| 源端负载 | 只读副本 + 令牌桶限速；源端延迟指标超阈值自动降速 |
| 大表几百 TB | 分区/pk 范围切片，数千块并行；按目标端写入吞吐反推并发 |
| schema 不兼容事件 | 该表暂停 apply、告警，事件留在流里不丢 |

规模估算：1 PB ÷ 250 MB/块 ≈ 4×10⁶ 块；全量以每小时 10 TB 计约 100 小时量级——所以**全量必须可暂停可恢复、按表逐步接入**，不是一次性。

## 5. 分层与组件

```
控制面：表注册 · 阶段状态机 · 调度/限速 · schema registry · 校验调度
数据面：CDC reader（每源实例 1 个，按 LSN 读日志）→ 持久化变更流（按 table/pk 分区）
        全量 chunk worker（无状态，读副本写 staging）
        apply worker（无状态，按分区消费，MERGE 到目标）
        verifier（只读，分块 checksum 双端比对）
```
唯一强一致状态：`table_sync_state` 与 `backfill_chunks`。其余组件无状态、可水平扩展。

## 6. Rollout / 测试 / 监控

- **接入新表**：先同步到影子表 → verifier 全表对账 → 切读流量；与我在 Braintree 把 interchange 取数从 Trans View 切到 Settle View 时做的 13.7M 行 day-level 对账（0.224% 差异逐类解释后才切）是同一套路。
- **监控**：每表 `lag = source.current_lsn - applied_lsn`（换算秒）；积压深度；apply 错误率；校验不一致行数；源端副本延迟。
- **测试**：故障注入（杀 chunk worker、杀 apply worker、重放重复事件、乱序事件）后断言收敛；schema 演进回放测试。
- **回滚**：目标端保留时间点快照，出错时切回上一个已校验快照。

## 7. 用 Snowflake 自己的原语作参照

目标端若是 Snowflake：apply 用 **Snowpipe Streaming**，每个 channel 带 **offset token**（就是这里的 LSN 位点），重连时从 token 继续，天然给出 exactly-once 的摄取语义；接入侧可用 **Openflow** 的 Oracle/PostgreSQL CDC 连接器。回滚与对账可用 **Time Travel / zero-copy clone**：对账前 clone 一份目标表，出错时回到对账通过的时间点。源端若是 **Snowflake Postgres**（2026-02 GA），这正是它向分析侧同步数据的问题本身。

## 8. 45 分钟口述时间表

| 分钟 | 内容 |
|---|---|
| 0–2 | 假设声明 + 四个不变量 + 不做什么（不许澄清，所以自己说） |
| 2–8 | 变更事件格式与每表状态模型 |
| 8–18 | 快照 + 增量拼接：snapshot_lsn、分块全量、缓冲增量、LSN 比较 MERGE |
| 18–28 | 失败模式表：崩溃续传、乱序重复、日志保留不足、热表、源端保护 |
| 28–35 | schema 演进与删除 |
| 35–40 | 校验与监控：分块 checksum、lag 指标、影子表灰度 |
| 40–45 | Snowflake 原语参照 + 自己的对账经历 + 反问 |
