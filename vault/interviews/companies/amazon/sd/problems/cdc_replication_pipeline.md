# 题 1：托管 CDC 复制管道（DMS 风格）

> 题库里**没有**这道题（已核对 `drills/problems/` 47 题；最近的是 [design-message-queue](../../../../../domains/system-design/drills/problems/design-message-queue.md) 与 [design-ad-click-aggregation](../../../../../domains/system-design/drills/problems/design-ad-click-aggregation.md)，但它们都不处理"从客户的源数据库里取变更"）。
> 先读 `../00_ddia_refresh.md` §6（日志/CDC/exactly-once），并复习卡 [async-cdc-mechanism](../../../../../domains/system-design/cards/async/async-cdc-mechanism.md)、[async-cdc-initial-snapshot](../../../../../domains/system-design/cards/async/async-cdc-initial-snapshot.md)、[correctness-dual-write-problem](../../../../../domains/system-design/cards/correctness/correctness-dual-write-problem.md)。
> 时间：45–60 分钟。研究依据：AWS DMS CDC 文档（https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Task.CDC.html ，2026-10-15 抓取）、
> Netflix DBLog 论文（https://arxiv.org/abs/2010.12597 ，2026-10-15 抓取摘要）、DynamoDB ATC'22（归档 WAL、校验）。

## 1. 题面（面试官会这样说）

> "设计一个**托管的数据库复制服务**：客户指定一个源数据库（MySQL / PostgreSQL / Oracle）和一个目标（另一个数据库、S3、Kinesis/Kafka、数据仓库）。
> 服务先做一次**全量迁移**，然后持续把源库的**变更**应用到目标，直到客户停止。服务要同时托管成千上万个客户的复制任务。"

## 2. 需求（你应该问出来并写在白板上）

**功能**
1. 创建/启动/暂停/恢复/停止"复制任务（task）"；任务 = 源端点 + 目标端点 + 表选择与转换规则。
2. 任务类型：仅全量（full load）、全量 + CDC、仅 CDC（从指定位点开始）。
3. 目标端可选 DB（按主键 upsert）、对象存储（追加变更文件，带操作类型列）、流（每行变更一个事件）。
4. 支持 schema 变化的策略（透传 / 忽略 / 暂停）、列过滤与重命名、数据校验（validation）。
5. 可观测：源端延迟、目标端延迟、已应用事务数、错误表。

**非功能**
- **不丢**（at-least-once 到目标）；**可重放幂等**（重复应用不改变结果）。
- **同一行的变更按源端提交顺序生效**（至少）；跨行/跨表顺序视目标而定。
- 对源库影响小：不加锁，不在源库上增加显著 CPU/IO；**每个源只读一份日志**。
- 延迟：**没有硬 SLA**。DMS 文档原文："AWS DMS CDC does not provide real-time replication … There are no SLAs for CDC latency … can increase to several minutes or longer"。
  所以面试里要先说清：我们承诺的是**正确性与可观测的延迟**，不是固定的延迟数字。
- 多租户：一个客户的大事务/高流量不能影响别人；任务故障自动恢复。

**非目标**：双向冲突解决（可作为追问）；跨目标的分布式事务；对源库做 schema 迁移。

## 3. 估算（数字由脚本算出，假设已标出）

| 量 | 计算 | 结果 |
|---|---|---|
| 活跃任务 | 假设 | 5 万个 |
| 平均变更速率 | 每任务 100 事件/s | 总 **500 万事件/s** |
| 平均事件大小 | 500 B（行前后镜像 + 元数据） | **2.5 GB/s** 总吞吐 |
| 重任务 | 单任务 5 万事件/s | 25 MB/s（一个任务就能吃满一个小 worker）|
| worker 数 | 假设一个 worker 稳定处理 2 万事件/s，目标利用率 50% | ≈ **500 个 worker**（最少 250）|
| 全量迁移 | 1 TB 表，8 路并行，每路 50 MB/s | 2,500 s ≈ **42 分钟** |
| 源端日志保留 | 5k 事件/s × 1 KB | 18 GB/小时；保留 7 天 ≈ 3 TB（**延迟必须小于日志保留期**）|
| checkpoint 写 | 每任务每 5 s 一次 | 约 **1 万次/s**（要选合适的存储）|

**这些数字改变了什么设计**：(1) 总吞吐不大但**任务数多且倾斜** → 以"任务"为调度单位，worker 池多租户混部，重任务单独隔离；
(2) 日志保留是**硬约束** → 延迟告警要早于保留期，超过就只能重新全量；(3) checkpoint 1 万次/s → 不能每个都写强一致慢存储，要批量/异步，并接受"重放一小段"。

## 4. 标准答案（senior 深度）

### 4.1 总体架构：控制面 / 数据面

```
控制面 (低频, 强一致)                            数据面 (高频, 水平扩展)
┌──────────────────────────────┐          ┌─────────────────────────────────────────────────────┐
│ API: CreateTask(client_token)│          │ Replication worker (一个任务 = 一个单例"所有权")      │
│ 元数据库: task, endpoint, 状态 │ 分配     │                                                     │
│ 调度/放置: task → worker      ├─────────▶│ [源 reader]──▶[变更缓冲]──▶[转换/过滤]──▶[apply 器]──▶ 目标 │
│ 租约 + fencing token         │ 心跳      │  读事务日志    内存+溢写盘   列映射/表规则   批量/幂等写    │
│ 监控/自愈: 失败检测、重放置    │◀─────────│      ▲                                     │         │
└──────────────────────────────┘          │      └────────── checkpoint(位点) ◀────────┘         │
                                          └─────────────────────────────────────────────────────┘
                 全量迁移 worker 池 (分块并行 SELECT, 与 CDC 交错, 见 §4.3)
```

关键设计选择：
1. **一个任务同一时刻只有一个 worker 持有所有权**（单例）。所有权靠**租约**，并发放 **fencing token**：
   apply 器写 checkpoint 和目标时带 token，旧 worker（GC 暂停、网络分区后"复活"）的写会被拒绝。（复习 [distributed-fencing-tokens](../../../../../domains/system-design/cards/distributed/distributed-fencing-tokens.md)、[distributed-epoch-numbers](../../../../../domains/system-design/cards/distributed/distributed-epoch-numbers.md)。）
2. **位点（position）是一等公民**：MySQL = (binlog 文件, 偏移) 或 GTID；PostgreSQL = LSN + 复制槽；Oracle = SCN。
   checkpoint = "已安全应用到目标的最大位点"，存在**控制面 KV**（按任务分区）并——对 DB 目标——**同事务写入目标库的控制表**（见 4.4）。
3. **源端的日志读取靠引擎原生接口**（Oracle LogMiner/binary reader，MySQL row 级 binlog，PostgreSQL 逻辑解码），需要客户在源端做配置（DMS 文档：Oracle 要开 supplemental logging，MySQL 要 row-level binlog）。
   → 面试时说清**前置条件**，这是产品能力边界。
4. **缓冲**：reader 与 apply 之间用**有界队列**（内存为主，超限溢写到本地盘）。背压向上游传导，但**不能让 reader 停止读日志太久**（否则源端日志堆积，甚至被轮转掉）。

### 4.2 数据模型（控制面）

```
Task      (task_id PK, account_id, src_endpoint, dst_endpoint, mode, table_rules, state, version, owner_worker, lease_expiry, fencing_token)
Checkpoint(task_id PK, position, applied_txn_count, updated_at, token)      -- 高频写,按 task_id 哈希分区
TableState(task_id, table, phase ∈ {pending, full_load, cdc, error}, last_pk, rows_loaded)
```
- 分区键：`task_id`（分布均匀）；二级索引 `account_id`（列出某客户任务；异步更新即可，最终一致）。
- `Task.version` 乐观并发控制（CAS）：状态机转换 `UPDATE … WHERE version = ?`；API 带 `client_token` 保证重试幂等。

### 4.3 全量 + CDC 的衔接：不丢、不重、不锁（本题最核心的深挖）

**朴素做法的问题**：先全量、后 CDC —— 全量期间发生的变更怎么办？先 CDC、后全量 —— 全量读到的行可能比日志更新（新），又被旧日志事件覆盖。

**做法 A：先记位点，再快照，再回放（有一致性快照时）**
```
1. 在源端记录当前日志位点 P0 (并保证日志从 P0 起不被清理: PG 复制槽 / MySQL 保留 binlog)
2. 以一致性快照读 (如 MySQL REPEATABLE READ + 事务开始时的位点, PG 导出快照) 做全量
3. 全量完成后，从 P0 开始应用日志；日志里"早于快照"的事件会重复应用，靠 *主键 upsert 幂等* 吸收
```
**做法 B：DBLog 式水位线（无锁、可暂停、不依赖长事务快照）** —— Netflix DBLog（arXiv 2010.12597；摘要已核对："watermark based approach … interleave transaction log events with rows that we directly select from tables … does not use locks"，按块 select、可暂停恢复；下面的低/高水位步骤细节我凭记忆写，`【凭记忆，面试前对照论文 §3 核对】`）：
把表按主键**分块**；对每一块：
```
写一条 "低水位" 标记到源库的某张水位表 → 日志里出现 LW 事件
SELECT 这一块的行（普通查询，不加锁）
写一条 "高水位" 标记 → 日志里出现 HW 事件
在 LW..HW 之间日志里出现的、主键落在本块内的变更 → 丢弃块内对应行的旧值（日志事件更新、以日志为准）
然后把"块结果 − 被覆盖的行"插入输出，*夹在日志事件流中间*
```
好处：(1) **日志处理不被全量阻塞**，随时可暂停/恢复；(2) 对源库无锁、影响小；(3) 可对任意表/任意主键再次触发（"重新同步某几行"）。
代价：需要在源库有一张可写的水位表（写权限），并且表必须有主键。

**senior 要补的细节**：
- 无主键的表怎么办？用所有列做逻辑键（性能差）或拒绝/降级为只支持追加；
- 大表全量需要**分块并行 + 断点续传**（`TableState.last_pk`），否则 42 分钟的任务中途失败就重来；
- 全量与 CDC 对同一表**共享目标写入的幂等性**（同一主键 upsert，后到的更新不覆盖更新的版本：用源端提交位点作为 `version`，目标端 `WHERE incoming_pos > current_pos`）。

### 4.4 "恰好一次"的真实含义：至少一次 + 幂等应用

```
读日志(位点 p)  ─▶ 转成变更事件 e(p) ─▶ 批量写目标 ─▶ 写 checkpoint(p)
崩溃点 ①: 写目标之前   → 重启从旧 checkpoint 重读 → 无重复
崩溃点 ②: 写目标之后,写 checkpoint 之前 → 重启会 *重放* 这批 → 目标必须幂等
```
- **DB 目标**：按主键 upsert / delete；`checkpoint` 与数据在**同一个目标库事务**里提交（把位点写进目标库的一张控制表），则崩溃后可从目标库读出"真正已应用到的位点"，应用侧"恰好一次"。
  （DMS 在目标库建控制表的做法我凭记忆写 `【凭记忆，面试前核对】`；这个"位点与数据同事务"的模式本身是标准做法。）
- **对象存储目标**：写不可变的文件，文件名含任务 id + 起止位点（确定性命名）。重放写出**同名同内容**文件，覆盖无副作用；下游读者按位点去重。
- **流目标（Kinesis/Kafka）**：天然至少一次；事件带 `(source_id, position)` 作为幂等键，消费者去重（见 [correctness-idempotent-consumer-patterns](../../../../../domains/system-design/cards/correctness/correctness-idempotent-consumer-patterns.md)）。
- **批量合并（net changes）**：同一批里同一主键的多次变更可合并成最后一条（INSERT+UPDATE → INSERT；INSERT+DELETE → 无），吞吐高但**丢失中间状态**（审计型目标不能用）。

### 4.5 顺序与并行

- 源端日志是**全序**的。apply 的并行度由目标决定：
  - **按事务串行**应用：最安全，吞吐受限（单线程）。
  - **按主键哈希并行**（同一行永远进同一个通道）：保证**行级顺序**，吞吐可扩展。跨表外键/跨行约束可能被临时违反 → 目标端延后校验约束或按表依赖分层应用。
- 大事务：一个事务可能含 1 亿行变更，不能全放内存 → 溢写盘，且**直到提交才对下游可见**（常见引擎按提交顺序输出已提交事务；PostgreSQL 较新版本可选择流式输出进行中的大事务，此时下游必须能处理回滚，`推断`，面试前核对）。
- 发生 **DDL** 的日志位置要作为"屏障"：先排空之前所有变更，再应用 DDL，再继续。

### 4.6 故障与自愈（逐层）

| 故障 | 检测 | 处理 |
|---|---|---|
| worker 进程崩溃 | 租约过期（比如 30 s）| 控制面把 task 分配给新 worker，**fencing token+1**，从 checkpoint 恢复 |
| worker 灰色故障（能心跳但 apply 很慢）| 延迟指标（apply 位点落后）| 主动迁移 task；不要仅靠心跳判活（[DDB22] §6.2 的"问其他副本"思想）|
| 目标不可用 | apply 重试失败 | 指数退避+抖动，**但 reader 继续读**到缓冲上限，之后暂停读（并告警：源日志保留倒计时）|
| 源日志被轮转（lag > 保留期）| 位点不存在 | **无法恢复** → 任务标记 `needs_full_reload`，必须重新全量 |
| 源库切主（failover）| 连接失败/位点不连续 | 需要 GTID/等价物才能接续；否则只能重新全量（面试里要承认这个限制）|
| 控制面故障 | — | **静态稳定**：已在运行的 worker 靠本地租约续期缓存继续工作，只是不能创建/变更任务 |

### 4.7 多租户与运维

- **放置**：worker 池按"重任务/普通任务"分池；任务按 `account_id` 做 **shuffle sharding**（每个账号只落在 pool 中的 k 个 worker 上），坏账号（超大事务、无限重试）不会拖垮所有人（[reliability-shuffle-sharding-mechanism](../../../../../domains/system-design/cards/reliability/reliability-shuffle-sharding-mechanism.md)）。
- **配额**：每账号任务数、总吞吐、源端连接数；API 层 token bucket。
- **对源库的保护**：每个源端点限制并发连接；全量读取限速（由客户指定"最大读取 MB/s"）。
- **发布**：worker 软件 one-box → 按 cell（账号分片）灰度 → bake → 自动回滚（见 `../00_how_to_run_the_round.md` §7.1）。**协议演进**用"先读后写"两阶段（checkpoint 格式、控制表格式的升级都要向后兼容）。
- **指标**（每任务）：`SourceLatency`（读到的最新事件时间与现在的差）、`TargetLatency`（已应用位点对应的源端时间与现在的差）、`ApplyThroughput`、`BufferBytes`、`ErrorTableRows`。
  **注入心跳**：在源库定期写入一行心跳（带时间戳），目标端看到它就得到端到端延迟——解决"源端没有写入时延迟看起来一直是 0 或无限"的问题。
- **数据校验（validation）**：按主键范围分块比较行数与校验和（源 vs 目标），异步运行，结果入错误表；不要在热路径做。

## 5. 追问与答案

**Q1. 你说"恰好一次"，具体是哪个边界？**
A：边界是**目标端状态**。传输层是至少一次，我用"主键 upsert + 位点作为版本"保证重放无副作用；对 DB 目标把位点与数据放进同一目标事务，则恢复时以目标库里的位点为准。对流目标则只是至少一次 + 消费者幂等，不能说成 exactly-once。

**Q2. 全量期间源表一直在写，你怎么保证目标最终与源一致？**
A：见 §4.3。做法 A 用一致性快照 + 位点 P0 之后回放，重复由幂等 upsert 吸收；做法 B（DBLog）用低/高水位在日志流中夹入块结果，对块内主键以日志为准。关键不变量：**任何一行最终取值 = 其最后一条日志事件，若无日志事件则为快照值**。

**Q3. 复制延迟已经 3 小时，源端 binlog 只保留 2 小时。**
A：位点已不存在，**不可恢复**，只能重新全量。预防：延迟告警阈值设为保留期的 25–50%；任务暂停时让源端保留日志（PG 复制槽会无限保留日志而撑爆磁盘 → 必须设上限和告警，这是 PG 复制槽的经典事故）；产品上把"日志保留期"作为接入检查项。

**Q4. 一个事务改了 1 亿行怎么办？**
A：reader 把事务缓冲到溢写盘；在提交位点之前不向 apply 释放；apply 时按主键分批 + 并行；checkpoint 只在"事务边界"推进，所以崩溃后重放整个事务（幂等）。需要限制单事务最大缓冲，超限则让任务进入 `error`，让客户拆分或调大资源。

**Q5. 源表发生 `ALTER TABLE ADD COLUMN` / 改类型 / 重命名？**
A：DDL 作为日志屏障。策略：加列 → 透传（目标先加列，再应用后续变更）；改类型 → 视兼容性（拓宽安全，收窄需要暂停）；重命名 → 对日志里按"位置"而非"名字"的格式有歧义，通常暂停并要求人工确认。核心原则：**先让下游能读新格式，再让上游写新格式**，与 DynamoDB 的 read-write deployment 同理（[DDB22] §6.4）。

**Q6. 同一行高频更新（热行），按主键哈希并行会怎样？**
A：同一行永远进同一个通道 → 串行，成为单通道瓶颈。缓解：批内合并（只应用最终状态）；目标端使用"最后写入胜出的版本号"，允许跳过中间版本。代价是丢失中间历史（审计场景不可用）。

**Q7. 如何防止一个客户的任务拖垮共享 worker？**
A：(1) cgroup 级 CPU/内存/磁盘限额；(2) 任务按吞吐分级，重任务独占池；(3) 账号 shuffle sharding；(4) 对溢写盘与缓冲大小设硬上限；(5) 任务异常（反复崩溃循环）指数退避并最终自动暂停，避免占用调度资源。

**Q8. 怎么做到控制面故障时已有任务继续跑？**
A：数据面只依赖本地租约+缓存的任务配置；checkpoint 写入目标侧或独立 KV。控制面只负责"创建/变更/放置"。要刻意测试：断开控制面，已有任务延迟指标不恶化（静态稳定，Builders' Library《Static stability using Availability Zones》）。

**Q9. 目标是 S3，客户想要"当前状态快照"而不是变更流？**
A：CDC 文件是**变更日志**（带 op 列 I/U/D 与提交位点）。当前状态 = 对日志按主键取最后一条并去掉 D。做法：下游定期 compaction/merge（Iceberg/Hudi 的 merge-on-read），或让目标直接写入支持 upsert 的表格式。这是"日志 → 物化视图"的标准模式（[async-materialized-view-refresh](../../../../../domains/system-design/cards/async/async-materialized-view-refresh.md)）。

**Q10. 你怎么知道复制是对的？**
A：三层：(1) 行数+分块校验和的 validation；(2) 端到端心跳延迟；(3) 抽样回读比对。再加"对账"思想：长期运行的 CDC 任务必有漂移（[correctness-reconciliation](../../../../../domains/system-design/cards/correctness/correctness-reconciliation.md)）。

## 6. 评分表

| 维度 | Strong | OK | Weak |
|---|---|---|---|
| 需求 | 先点出"CDC 没有延迟 SLA"，把正确性与可观测性当产品承诺；问源库类型与日志前提 | 问了源/目标类型 | 把它当"读表写表"的 ETL |
| 全量与增量衔接 | 能讲位点+快照回放，**或** DBLog 水位线；说清不变量 | 说"先全量再增量"并想到去重 | 忽略全量期间的写入 |
| 正确性 | 位点与数据同事务/确定性文件名；幂等 upsert；明确 exactly-once 边界 | 说"at-least-once + 去重" | 声称"我们保证 exactly-once"无细节 |
| 顺序与并行 | 行级顺序+主键哈希并行；DDL 屏障；大事务 | 提到顺序 | 全部串行或全部并行不谈顺序 |
| 故障 | 租约+fencing；灰色故障；日志轮转不可恢复；控制面静态稳定 | 重试/重启 | "挂了就重启" |
| 多租户与运维 | shuffle sharding、配额、对源库保护、心跳延迟、one-box 发布 | 提到限流 | 无 |
| 取舍意识 | 主动讲净变更合并 vs 保留历史、吞吐 vs 顺序 | 被动回答 | 只给单一方案 |

**Senior 常见失分点**：不提日志保留约束；把 DMS 说成"实时"；无主键表不考虑；checkpoint 与数据分开写却说 exactly-once。

## 7. 与题库的关系
- 概念：[design-message-queue](../../../../../domains/system-design/drills/problems/design-message-queue.md)（分区日志、消费者位点）、[design-ad-click-aggregation](../../../../../domains/system-design/drills/problems/design-ad-click-aggregation.md)（幂等 upsert key、对账）。
- 更进一步：[map:async.streaming.cdc](../../../../../domains/system-design/map/async.streaming.cdc.md)、[turning-the-database-inside-out](../../../../../domains/system-design/readings/turning-the-database-inside-out.md)。
