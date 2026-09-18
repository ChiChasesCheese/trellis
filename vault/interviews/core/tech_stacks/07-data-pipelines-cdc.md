---
title: TS07 · 数据管道与 CDC
aliases:
  - TS07
  - 数据管道与 CDC
tags:
  - interview/stack
  - stack/data-pipelines
  - stack/kafka
stories: [S1, S5, S11]
---

# 07 · 数据管道与 CDC（Data Pipelines & Change Data Capture）

> 知识层（想更深时去哪）：[[System Design MOC|system-design]]：[[async.streaming.cdc]] · [[async.streaming.processing]] · [[analytics.batch]] · [[analytics.derived]] · [[correctness.outbox]]；[[Kafka MOC|kafka]]：[[connect.pipeline-design]] · [[connect.connect-basics]] <!-- domain-links -->
> 适用于：JD 上出现 data pipeline / ETL / ELT / CDC / Debezium / Kafka Connect / Airflow；被问"你们的数据是怎么从 A 到 B 的"。
> 不适用于：流式计算引擎本身的深度（Flink 的 watermark、state backend）——见第 5 节。

---

## 0. 这个栈在 JD 里到底在问什么

写"data pipeline"的 JD，面试官心里通常是三个问题里的一个：

**一、你搬过数据没有，还是只查过数据。** 区别在于有没有处理过"上游改了、下游要跟上"这件事。查数据的人只面对一个稳定的表；搬数据的人要面对表在变、schema 在变、上游挂了、文件迟到了。

**二、你知不知道"把数据从 A 复制到 B"有多容易出错。** 这是最核心的一问。天真的答案是"起个定时任务 select 出来 insert 进去"，而所有真实的坑都在这个答案里：重跑会不会重复、漏了怎么补、上游删了行下游知不知道、跑到一半挂了算什么状态。

**三、你能不能说清批和流的取舍。** 能说出"我们这条走批那条走流，因为……"的人，比只会说"流比批先进"的人强一个档次。

---

## 1. 来龙去脉

### 1.1 双写：那个看起来能用、实际上一定会坏的做法

假设你有一个订单服务，数据在 MySQL 里。现在搜索团队想要订单数据进 Elasticsearch。最直觉的写法：

```python
def create_order(order):
    mysql.insert(order)          # 第一次写
    elasticsearch.index(order)   # 第二次写
```

这叫**双写（dual write）**，它一定会坏，原因不止一个：

- **部分失败。** 第一行成功、第二行抛异常（ES 超时、网络抖动、进程被 kill），两个系统从此不一致，而且没人知道。你可以加 try/except 重试，但重试也可能失败；你可以加事务，但 MySQL 的事务管不到 ES。
- **并发下的顺序错乱。** 两个请求几乎同时改同一个订单：A 先写 MySQL、B 后写 MySQL，但 B 先到 ES、A 后到 ES。MySQL 里是 B 的值，ES 里是 A 的值。两个系统各自都"没出错"，合起来却错了。
- **没有真相来源。** 不一致发生后，你没法回答"谁是对的"。没有一份记录说明这两次写本来应该是一回事。

这不是工程能力不足的问题——**没有跨系统的分布式事务，双写在原理上就无法保证一致**。而分布式事务（2PC）的代价在大多数场景下高到不可接受（见 [[10-correctness-idempotency]] 第 1 节）。

### 1.2 CDC 的核心洞察：数据库已经有一份完美的变更日志了

关键的转念是：**别写两次，写一次，然后把那一次"广播"出去。**

任何支持崩溃恢复的数据库，内部都有一份按顺序记录所有变更的日志——MySQL 的 binlog、PostgreSQL 的 WAL、MongoDB 的 oplog。这份日志的性质恰好是我们想要的：

- **它是真相。** 数据库自己靠它恢复，所以它一定和表的最终状态一致，不存在"日志说的和表里的不一样"。
- **它有序。** 日志是单一的、全序的，天然解决了 1.1 里的并发顺序问题。
- **它完整。** 增、删、改都在里面，包括删除——这一点后面会看到很重要。
- **它已经在那了。** 不需要改业务代码，不需要加字段，不需要应用配合。

**Change Data Capture（变更数据捕获）就是读这份日志，把变更事件发给所有需要的下游。** 业务代码只写一次数据库，其余系统订阅变更流。不一致的可能性被消除了，因为不再有"第二次写"。

这个思路还有个漂亮的推论：**数据库的当前状态，等于从空表开始把所有变更重放一遍的结果**。表是日志的物化视图，而不是相反。一旦接受这个视角，"再加一个下游"就变成了"从日志的某个位置开始重放"，而不是"再写一次"。

### 1.3 log-based vs query-based：为什么前者几乎总是对的

CDC 有两种实现路线，差别很大：

| | query-based（轮询） | log-based（读日志） |
|---|---|---|
| 做法 | 定时 `SELECT * WHERE updated_at > :last` | 解析 binlog / WAL |
| 改不改上游 | 要有 `updated_at` 列，且必须维护对 | 不用动上游 |
| **删除** | **捕获不到**（行没了，查不出来） | 捕获得到 |
| 中间态 | 丢失（一个周期内改三次只看到最后一次） | 每次变更都在 |
| 上游压力 | 每次轮询一次全表扫或索引扫 | 几乎为零（读日志文件） |
| 延迟 | 取决于轮询间隔 | 秒级以下 |

**捕获不到删除**这一条通常就足以否决 query-based。下游会留下永远不会消失的幽灵行，而且没有任何信号告诉你它们该走了。绕过的办法是软删除（`deleted_at` 列）——但那是在改上游的数据模型来迁就下游的管道，方向反了。

log-based 的代价是运维复杂度：要接数据库的复制协议（Debezium 干的就是这件事），要处理日志轮转、位点保存、大事务、schema 变更。所以小规模场景里 query-based 仍然常见——但要清楚自己放弃了什么，而不是不知道有这回事。

### 1.4 Outbox：当你必须让应用参与时

CDC 捕获的是**表的变更**，但有时你想发的是**业务事件**。"订单表的 status 字段从 2 变成 3"和"订单已发货"不是一回事——后者携带了前者没有的语义，而且下游不该去理解你的状态码枚举。

**Outbox 模式**解决这个：在同一个数据库事务里，业务写业务表，同时往一张 `outbox` 表插一条事件记录。

```sql
BEGIN;
  UPDATE orders SET status = 'SHIPPED' WHERE id = 42;
  INSERT INTO outbox (event_type, payload) VALUES ('OrderShipped', '{...}');
COMMIT;
```

两次写在**同一个事务**里，所以要么都成功要么都失败——这不是双写，这是一次写。然后用 CDC 去捕获 `outbox` 表，发出去。

它买到的是：事件的语义由应用决定，且事件的发出与业务状态的改变原子绑定。代价是多一张表、多一个清理任务，以及事件 schema 成了需要维护的契约。

### 1.5 批与流：那条一直在移动的边界

传统的划分是：批处理跑在有界的数据集上（"昨天全天的订单"），流处理跑在无界的数据流上（"订单来一笔算一笔"）。

真正的区别不在技术，在**你什么时候承认"数据齐了"**：

- 批处理有一个明确的窗口关闭点。到点了就算，晚到的数据进下一批或者触发重跑。逻辑简单，可以整体重算，错了重跑一遍就好。
- 流处理永远不敢说"齐了"。它必须处理迟到数据、乱序、水位线（watermark）、以及"我现在给出的结果可能被后续数据修正"。

边界在移动，是因为两边都在往中间靠：批处理的调度间隔越缩越短（一天 → 一小时 → 五分钟），流处理引入了微批和窗口。到某个点上，"每 5 分钟跑一次的批"和"5 分钟窗口的流"在业务上无法区分。

**所以选批还是流，真正的判据不是延迟，而是三件事：**
1. **正确性的定义需不需要一个明确的截止点。** 财务对账必须有——"这一天的账"是一个必须能封口的概念。推荐系统不需要。
2. **上游给你的是什么形状。** 上游一天甩一个文件，你做不成流；上游是 Kafka topic，你做成批反而要自己攒。
3. **错了怎么补。** 批的补救是重跑一个分区，代价可预期；流的补救是回放一段偏移量，要求整条链路幂等。

---

## 2. 在我们这套系统里它怎么用

这套系统里最值得讲的一点是：**同一个团队、同一个 Snowflake 平台，同时跑着两条形态完全不同的管道**，而且两条都是对的选择。把它们并排放在一起看，比单讲任何一条都有说服力。

### 2.1 两条管道并排看

| | **GRRCN 结算文件管道** | **Funding→Snowglobe CDC 管道** |
|---|---|---|
| 上游给什么 | Amex 每天甩一个定长文本文件到 S3 | Funding 的 MySQL 表持续变更 |
| 形态 | 文件批 | 日志捕获（Kafka CDC connector） |
| 入口 | `COPY INTO` from S3 stage | Kafka connector 写入 Snowflake 原始表 |
| 幂等靠什么 | Snowflake `COPY INTO` 的**文件级**去重（文件名 + checksum） | procedure 里的 **MERGE 业务键** |
| 解析在哪 | 下游 procedure 里的 `SUBSTRING`（定长切分） | UDTF 解析 JSON/variant payload |
| 失败姿态 | `ON_ERROR = 'ABORT_STATEMENT'`，整文件回滚 | 单行失败不阻塞后续 |
| 为什么是这个形态 | Amex 只给文件，没有别的通道 | 上游是活的数据库，要持续同步 |

**共同点比差异更有意思**：两条管道的下游编排用的是**同一套 Snowflake 原语** —— `STREAM` 检测新增行、`TASK` 在 `SYSTEM$STREAM_HAS_DATA(...)` 为真时唤醒、`PROCEDURE` 做实际的 merge。也就是说，入口形态的差异被吸收在第一跳，从第二跳开始两条路收敛成同一个模型。

这是个很好的架构决策，值得在面试里点出来：**把"数据怎么进来"和"数据进来之后怎么流"解耦**，前者随上游变，后者全公司统一。新接一个上游只需要写入口那一段。

### 2.2 GRRCN 文件管道：批处理的真实形状

**为什么必须是批。** Amex 在 OptBlue/Aggregated 模式下不像 Visa/Mastercard 那样提供准实时的 Trans/Settle 视图，它每天甩一个定长文本文件（GRRCN，Global Reconciliation）过来，里面才最终确认哪些交易真正结算成功、扣了多少 fee。上游形态决定了管道形态——这里没有"要不要做成流"的选择空间。

**Good Funds Model：批的语义决定了业务的语义。** 因为确认要等文件，Braintree 收到一笔 Amex 交易时**不能乐观入账**。交易先在 `pending_transactions` 里趴着，等 GRRCN 文件验真了才"转正"进 `transactions` 表，参与下游的对账、BT-Fee 计算和 Funding 出款。这是管道形态反过来塑造业务模型的例子——不是先有业务规则再选技术，是上游的物理约束决定了资金能多早被承认。

**入口：`COPY INTO` 与两个关键决策。**
（`app/src/main/resources/db/stored-procedures/pass_through_fees/R__load-amex-grrcn-file-to-staging-table.sql`）

```sql
COPY INTO AMEX_GRRCN_STAGING (...)
FROM (
  SELECT :grrcn_id, TRIM(LEFT($1, 10)) AS RECORD_TYPE, $1 AS RECORD_TEXT,
         METADATA$FILENAME, METADATA$FILE_ROW_NUMBER, CURRENT_TIMESTAMP()
  FROM @FUNDING_S3_STAGE/outbound/aggregated-amex/ (
    PATTERN => '^\d{4}-\d{2}-\d{2}/(amex_opt_blue_settlement_grrcn|amex_settlement_eur_grrcn).*$'
  )
)
FILE_FORMAT = (FIELD_DELIMITER = NONE RECORD_DELIMITER = '\n' SKIP_BLANK_LINES = TRUE)
ON_ERROR = 'ABORT_STATEMENT'
FORCE = FALSE;
```

第一个决策：**`PATTERN` 扫所有日期子目录，而不是只认今天。** 代码注释直接写了原因——文件可能落在昨天的目录里，而处理任务已经跑在今天了。这是从一次生产事故里补回来的教训（注释里挂着 Slack 链接）。这条特别适合在面试里讲：**"按今天的日期去找今天的文件"是一个看起来天经地义、实际上假设了上游和你共享同一个时钟的写法。**

第二个决策：**`FORCE = FALSE` 让幂等性由 Snowflake 的文件级去重兜底**（按文件名 + checksum），而不是业务字段 MERGE。procedure 注释写着 "Deletion and reload of the same file will not render new records"。这是批处理特有的便利——文件是天然的幂等单元，流式管道没有这个奢侈品。

第三个决策：**`ON_ERROR = 'ABORT_STATEMENT'` 是拿可用性换正确性。** 一个坏字符会挡住当天全部记录，但绝不会出现"半个文件生效"的脏数据。对结算数据，这个取舍是对的——半个文件的账比没有账更难救。

**分流：一张表，六条 append-only stream。** `AMEX_GRRCN_STAGING` 被 6 条 stream 各自订阅（按 `RECORD_TYPE` 分成 transactions / transaction_pricing / adjustments / chargebacks / fee_revenue / summary），每条挂一个下游 task 并行消费。

用 `APPEND_ONLY = TRUE` 而不是标准 stream，是因为标准 stream 靠变更追踪生成"净变化"行、重试语义复杂；而一张只增不改的落地表配 append-only stream，语义退化成"游标往前走"，多个消费者各自维护偏移量、互不干扰。**要让 N 个下游从同一张表分流，append-only 是最省心的模型。**

代价是它不防重放：stream 的 offset 一旦被消费就不会回退，task 内部逻辑失败但 DML 提交了位点，数据不会重来。**正确性最终靠下游 processor 里 MERGE 的幂等键兜底，而不是靠 stream 本身** —— 这个分层很重要，stream 负责"有没有新数据"，幂等键负责"处理对不对"。

**一个值得讲的文档与代码不一致。** 设计文档（Confluence pageId `2233926829`）把解析步骤描述为 `PARSE_AMEX_GRRCN_TRANSACTIONS()` 这类 UDTF，但代码里**不存在**这些 UDTF——真正的定长解析是写死在 6 个 `PROCESS_AMEX_GRRCN_*` stored procedure 内部的 `MERGE ... USING (SELECT SUBSTRING(...))`。文档先行、实现时改了形状、没回填。面试里被问"文档和代码不一致怎么办"，这是现成的真实例子：**以代码为准，然后把文档修了**。

### 2.3 Funding→Snowglobe CDC 管道：日志捕获的真实形状

上游是 Funding 的业务表（`pricing_schedules`、`pricing_schedule_fees` 等），它们是活的、持续变更的。这里没有文件可等，形态自然是 CDC。

链路：**Kafka CDC connector → Snowflake 原始表 → `snowflake_stream_on_table` → `snowflake_task`（`system$stream_has_data(...)` 触发）→ `snowflake_procedure_sql` merge/upsert → 类型化目标表**，配一个 `snowflake_function_sql`（UDTF）解析原始 JSON/variant payload。

整条链路是 Terraform 声明出来的，集中在 `modules/cdc/main.tf`（单文件近 4000 行）。这里有个细节值得注意：**`modules/cdc/main.tf` 里有指向 funding 仓库具体 commit SHA 的注释** —— 那是这两个仓库之间最实锤的物理连接点。跨仓库的契约没法靠类型系统保证，只能靠这种手写的锚点，而它会过期。

**为什么这条要 MERGE 而不能靠文件去重。** 上游是持续的行级变更，没有"文件"这个天然幂等单元，所以幂等必须落到业务键上。这正好对上 1.3 那张表——log-based CDC 买到了删除捕获和低延迟，代价是你得自己设计幂等。

**JSON payload 与 schema 演化。** CDC 事件是 JSON/variant，UDTF 负责解析成类型化的列。这个中间层不是多余的：它是 schema 演化的缓冲区。上游加一个字段，原始表不用改（variant 装得下），UDTF 和目标表可以晚一点跟上，管道不会因为上游发布而断。这是 [[correctness.outbox]] 和 schema-on-read 思路的现实体现。

### 2.4 我做的部分 `[me]`

GRRCN 那条管道是我端到端做的，锚点 PR：**#751**（eventstream → pending_transactions 摄入）、**#856**（文件落地 + stream 建立）、**#862**（GRRCN 表 DDL）、**#886**（1,849 行，六种记录类型的解析与处理任务，我最大的一个 PR）、**#911**（校验 + 迁移进 transactions）、**#1023**（BT-Fee 计算与错误重试），外加约 10 个加固 PR。设计文档 Confluence `2233926829` 也是我写的。EU 扩展（`amex_settlement_eur_grrcn`）在摄入层的正则、以及那条"扫所有日期目录"的事故修复，都在这条线上。

原始证据：[[S1]]、本机 `raw/repo-snowglobe`。

**CDC 那条管道不是我建的**，它在 `snowglobe-terraform` 仓库里由团队维护，我在那个仓库只有 5 个 PR，主要是 grant/ownership 方向（见 [[S8]]）。我对它的了解来自读代码和作为下游消费者，不是来自建它。这个区别在面试里要讲清楚——讲系统可以讲全貌，讲"我做的"必须收窄。

---

## 3. stripe kit 考到的点

OA 里不会直接问 CDC，但管道的**内核**是高频考点，因为一道多 part 的题本质上就是一条微型管道：

- [[s19-incremental-design-parse-model-compute-render|S19 增量式设计：parse → model → compute → render]] —— 这正是管道的四段式，只是跑在一个进程里
- [[s02-line-oriented-parsing|S02 面向行的解析（分隔符、类型化字段、坏行）]] —— GRRCN 的定长解析是它的工业版
- [[s10-event-stream-reversal|S10 事件流 + 反向事件]] —— CDC 的 delete 事件就是反向事件
- [[s11-idempotency-dedup|S11 幂等 / 去重]] —— 重跑会不会重复，是管道和 OA 题共用的第一问
- [[s18-validation-error-paths|S18 校验与错误路径]] —— 对应 `ON_ERROR = 'ABORT_STATEMENT'` 那个取舍

反过来看也成立：OA 题里"第 4 part 引入撤销事件，要能反向修改前面的计数"，考的就是**你的中间状态留没留够信息**——和 CDC 管道里"只存聚合还是存明细"是同一个问题。

---

## 4. 常见追问与答法

| 追问 | 一句话答 | 展开的抓手 |
|---|---|---|
| 为什么不直接双写 | 没有跨系统事务，部分失败和并发乱序无法避免，而且事后无法判定谁对 | 展开 1.1 的三个失败模式 |
| CDC 和定时同步的区别 | 定时同步捕获不到删除，也丢中间态 | 1.3 那张对比表 |
| 上游 schema 变了怎么办 | 原始层用 variant 吸收，解析层晚一步跟上，管道不因上游发布而断 | 2.3 的 UDTF 缓冲层 |
| 管道跑挂了怎么恢复 | 分两层：批靠文件级幂等重跑，流靠业务键 MERGE 重放 | 2.1 表里"幂等靠什么"那行 |
| 怎么知道数据是对的 | 管道内的幂等只保证不重复，不保证不遗漏；遗漏要靠外层对账发现 | 接到 [[10-correctness-idempotency]] 的对账一节 |
| **（三层）append-only stream 消费失败了，数据会重来吗** | **不会。offset 推进和业务处理不是一个事务** | 所以正确性不能依赖 stream，必须靠下游幂等键。这是这套设计里最容易被误解的一点 |
| **（三层）如果 GRRCN 文件迟到三天** | **`PATTERN` 扫全部日期目录，迟到文件下次跑会被捡起；但那三天的下游计算已经出过一版少数据的结果** | 引出"批的补救是重跑分区"，以及为什么财务场景要能按天封口重算 |
| **（三层）这两条管道要合成一条吗** | **入口不能合，下游已经合了** | 2.1 的"解耦入口与流转"，正是这个问题的答案 |

---

## 5. 我的边界

**流式计算引擎本身我没做过。** Flink / Spark Streaming 的 watermark、state backend、exactly-once checkpoint，我能说清概念，没有生产经验。
→ 我会说："我做的流是 Snowflake 的 stream + task，它更接近微批而不是真正的流式计算——没有 watermark 和状态后端这套东西。Flink 那套我读过原理但没在生产上调过，如果这个岗位要深度用 Flink，我需要一段上手时间。"
→ 接回去："不过我处理过的乱序和迟到问题是真实的——GRRCN 文件迟到那个案例，本质上就是没有 watermark 时人工画的一条线。"

**Debezium / Kafka Connect 我是消费者不是建设者。** CDC 那条管道在团队的 terraform 仓库里，我读过、依赖它，但不是我搭的。
→ 我会说："那条管道我是下游。connector 的配置、位点管理、大事务处理这些运维面我没碰过，我熟的是它落地之后在 Snowflake 侧的 stream → task → merge 这段。"

**Airflow / Dagster 这类编排器没用过。** 我们的编排原语是 Snowflake 原生的 task DAG。
→ 我会说："我们没用 Airflow，调度是 Snowflake task 的依赖链（`AFTER <task>` + `WHEN SYSTEM$STREAM_HAS_DATA`）。概念上是一回事——有向无环图、依赖触发、失败重试——但 Airflow 的 operator 生态、backfill 机制、UI 那套我没实操过。"

---

## 6. 往深里看

| 节点 | 什么时候去读它 |
|---|---|
| [[async.streaming.cdc]] | 要讲 CDC 原理、Debezium 实现、log 位点管理时 |
| [[async.streaming.processing]] | 被问到流式计算、窗口、watermark 时（也是我第 5 节的补课方向） |
| [[analytics.batch]] | 要讲批处理的重跑、分区、幂等单元时 |
| [[analytics.derived]] | "表是日志的物化视图"这个视角的展开，以及物化视图的维护成本 |
| [[correctness.outbox]] | 双写与 outbox 的完整论证 |
| [[connect.pipeline-design]] | Kafka Connect 做管道的设计考量 |
| [[connect.connect-basics]] | Connect 的架构：worker、connector、task、offset |

相邻的两份：[[10-correctness-idempotency]]（幂等与对账，本文多处指向它）、[[02-kafka-event-streaming]]（日志与投递语义的上游）。

卡片和 readings 在 `vault/domains/system-design/cards/async/`、`vault/domains/kafka/cards/connect/`。
