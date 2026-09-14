# 评分 rubric（五维，1–4 分/维，满分 20）

> 这道题的特殊性：**不许澄清需求**。第一维因此不是"问对问题"，而是"自己声明对的假设"。

## 1. Problem framing（假设声明）

- **1 分**：沉默几十秒后问"数据库是什么类型？"被拒后卡住；或直接开始画"源库 → Kafka → 目标库"。
- **4 分**：开场 2 分钟内主动声明："I'll assume a transactional source with a change log (binlog/WAL), a columnar analytical target, target lag of minutes not seconds, at-least-once delivery with idempotent apply so the end state converges, and no downtime on the source." 并说出三个不变量：**源端不停写、断点可续、目标端最终与源端某个一致快照相同**；明确"不做"：不保证跨表事务在目标端的实时原子性、不做双向同步。

## 2. API & data model

- **1 分**：只有"表 → 表"的箭头；没有变更事件的格式；没有位点（offset/LSN）的概念。
- **4 分**：定义变更事件 `(table, pk, op, before/after, commit_lsn, txn_id, schema_version)`；每张表的同步状态 `(table, phase=backfill|catchup|streaming, snapshot_lsn, applied_lsn, backfill_cursor, schema_version)`；目标端 apply 用 `MERGE ON pk WHERE incoming.commit_lsn > target.last_lsn`（幂等 + 乱序安全）；一致性校验的接口（按 pk 范围分块 checksum）。

## 3. Failure modes & scale

- **1 分**：说"用 Kafka 就行了""失败重试"；没有意识到全量搬运和增量追赶之间有窗口。
- **4 分**：讲清**快照 + 增量拼接**：记下快照开始的 LSN，全量按 pk 分块并行搬，增量从该 LSN 开始缓冲，全量结束后回放增量（MERGE 按 LSN 去重覆盖）；**源端保护**：从只读副本或存储快照读、分块限速、按负载自适应；**断点续传**：每块完成写 cursor，崩溃后从最后完成的块继续；**大表**：按 pk 范围或分区切片、块大小 100–250 MB 文件；**schema 演进**：事件带 schema_version，加列前向兼容、改类型走影子列 + 回填；**删除**：tombstone 事件，目标端软删或 MERGE DELETE；**变更日志保留不够**（落后太多）：退回重做该表快照。

## 4. Separation of concerns

- **1 分**：一个"同步服务"包办读日志、搬全量、写目标、校验。
- **4 分**：分层：**控制面**（表注册、阶段状态机、调度与限速、schema registry）与**数据面**（CDC 读取器 → 持久化变更流（按表/pk 分区）→ 无状态 apply worker）分开；**全量搬运器**独立扩缩；**校验器**独立运行、只读、可旁路。

## 5. Delivery beyond the diagram

- **1 分**：画完就停。
- **4 分**：如何接入一张新表（灰度：先影子表对账再切读流量）；监控 = 每表 `applied_lsn` 与源端 `current_lsn` 的差（延迟）、积压、apply 错误率、校验不一致行数；校验 = 分块 checksum，不一致块重搬；回滚 = 目标端切回上一个一致快照（time travel / clone）。能说出"这就是我在 Braintree 做 Settle View 切换时 13.7M 行 day-level 对账的放大版"加分。
