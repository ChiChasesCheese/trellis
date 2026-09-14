# 卡片 · Snowflake 内部原语（SD / expertise / 反问 都用得上）

> 来源：`../../../01-company-brief.md` §1–§2（每条带官方文档或工程博客 URL，见 `../../../raw/company_research.md`）。格式 `| Q | A | 面试里怎么用 |`。**这些不是背诵题，是拿来当参照的**：设计题里说"这跟 Snowflake 自己的 X 是同一类问题"，是早期职业候选人最便宜的差异化。

## 架构

| Q | A | 面试里怎么用 |
|---|---|---|
| 三层架构分别是什么、为什么能拆开？ | 存储 = 不可变列式 **micro-partition**（50–500 MB）放对象存储；计算 = 独立 **virtual warehouse** 按秒计费；**Cloud Services（GS）** 无状态服务做认证/元数据/优化/事务，元数据全在 **FoundationDB**。数据不可变 + 元数据集中 ⇒ 多仓库同读不抢、存算独立伸缩 | KV store / 对象存储题：先分离"数据平面"和"元数据平面" |
| zero-copy clone 和 Time Travel 为什么几乎免费？ | 表 = FDB 里一份版本化的 partition 列表；clone 复制指针，time travel 读旧版本列表；默认 1 天、最长 90 天，之后 Fail-safe 7 天 | 版本化 KV / 快照题：MVCC + 不可变块 + 元数据指针 |
| Execution Anchor 是什么？ | 每个查询在生命周期内绑定到**恰好一个 GS 实例**，绑定存 FDB；进程内 guard 在每次 FDB 事务前校验；~99% 查询不转移；重试时"自愿转移"，崩溃时两阶段"非自愿转移"（心跳嵌入事务 + 恢复实例在 FDB 宣告终止后接管） | 任何"exactly-one-writer / lease / leader"题的现成参照；反问 §C 第一条 |
| 结果缓存三层？ | 持久化结果缓存（同 SQL + 数据没变，24 h 内直接返回，不起仓库）；仓库本地 SSD 缓存；元数据缓存（COUNT/MIN/MAX 走分区统计） | LRU/多级缓存题：od08 的 "SSD + 远端对象存储" 框架 |

## 流与调度

| Q | A | 面试里怎么用 |
|---|---|---|
| Stream 的本质？ | 一个 **offset 书签**指向表版本；查 stream 得净变化 + `METADATA$ACTION / ISUPDATE / ROW_ID`；**只有在 DML 事务里消费才推进 offset**；standard / append-only / insert-only；为防 stale 自动延长源表保留期到 14 天 | CDC / 幂等消费题：offset 只在事务内推进 = at-least-once 的正确形态 |
| Task 的调度模型？ | CRON 或间隔；可组 DAG（task graph）；`WHEN SYSTEM$STREAM_HAS_DATA()` 避免空跑；serverless（自动分配到 XXL）或自管仓库；`SUSPEND_TASK_AFTER_NUM_FAILURES`、`TASK_AUTO_RETRY_ATTEMPTS`、`TASK_HISTORY()` | sd02 / od05：cron 调度器的产品级参照；"部分失败语义"追问 |
| Dynamic Tables 解决了什么？ | 把 "stream + task + MERGE" 声明化：`TARGET_LAG`，自动推依赖图、增量 vs 全量刷新、按依赖顺序刷新、下游看一致快照；2026-07 Adaptive Refresh（上游大变动自动重初始化） | sd08 DAG 物化视图缓存 ≈ 这个；"何时退化成全量"是标准追问 |
| Snowpipe vs Snowpipe Streaming vs Datastream？ | 文件事件微批（分钟级）/ 行级 channel + offset token exactly-once（10 GB/s、5 s）/ Kafka wire-compatible 原生流（Summit 2026 预览） | ingestion 题、队列题的语义参照（offset token = 幂等键） |

## 事务与存储

| Q | A | 面试里怎么用 |
|---|---|---|
| Unistore / Hybrid Tables？ | 行存主表 + 强制 PK + 同步索引 + 行锁，毫秒点查；后台异步同步到列存；跨 hybrid 与普通表原子事务；事务引擎是 FDB | "结算 OLTP 放哪"——我有真实负载可比 |
| Snowflake Postgres？ | 真 Postgres 实例（Crunchy Data，~$250M，2025-06），独占 VM、PgBouncer、Private Link，2026-02-24 GA | OLTP 话题 / team matching 方向 |
| Iceberg / Polaris / Horizon？ | 开放表格式（v3：row lineage、deletion vectors）/ 开源 REST catalog（2026-02 Apache 顶级项目）/ 治理统一层（AI Agent Identity GA） | 外部引擎写 Iceberg 的三阶段提交（写数据 → 原子更新 catalog 指针 → 提交治理元数据）是分布式提交的好例子 |
| 计量与计费口径？ | credits 按秒、仓库 60 s 起；Cloud Services 每日免费 = 仓库消耗 10%；serverless 各有费率；AI 按 token（`METERING_HISTORY.SERVICE_TYPE='AI_SERVICES'`），2026-03 花费上限、2026-07 per-user 配额 | sd04 quota / billing 话题；我的"金融级对账 → 计量级对账"桥 |

## 产品与业务（一句话版，防被问懵）

| Q | A |
|---|---|
| CoCo / CoWork 是什么？ | Summit 2026-06-02 改名：CoCo = 原 Cortex Code（AI 编码 agent，9,100+ 账户）；CoWork = 原 Snowflake Intelligence（业务人员 agent，5,800+）|
| Cortex AI Gateway？ | 2026-07-28：统一管 agent → 模型/工具/MCP，团队级成本归集；2026-08-18 dynamic model routing |
| 最新季度数字？ | FY27 Q2（2026-09-02）：product revenue $1.49B +37%，连续三季加速；NRR 126%；FY27 指引 $6.07B；股价次日 +17% |
| 战略三句？ | AI 控制平面（三重飞轮）· 消费模型 + 模型中立（Anthropic $200M / OpenAI $200M）· 开放互操作 + OLTP 上移 |
| 近期事故？ | 2026-09-09 21:26–21:55 UTC 部分元数据基础设施不可用（status 页公开）—— 反问 FDB blast radius |
