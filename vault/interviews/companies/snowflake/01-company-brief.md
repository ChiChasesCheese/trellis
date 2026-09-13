# 01 · Snowflake 尽调（Backend SWE 视角）

> 精简版。每条的来源 URL 与日期在 `raw/company_research.md`（44 KB）里；本文件只留面试里**说得出口**的内容。财年口径：FY2027 = 2026-02-01 ~ 2027-01-31。

## 0. 一页速览（贴卡片）

- **是什么**：AI Data Cloud → 管理层现在叫「agentic enterprise 的控制平面」：governed data + 模型接入 + 应用工作流 + agent 控制面。消费模型（按 credits 计费）。
- **最新季度**（FY27 Q2，2026-09-02 发布）：product revenue **$1.49B，+37%**；连续第三个季度增速加速；NRR **126%**；$1M+ 客户 **828**；RPO **$9.0B**；FY27 指引上调到 **$6.07B（+36%）**；股价次日 **+17%**、盘中历史新高。AI 产品贡献了约一半的加速。
- **AI 产品名（2026-06-02 Summit 改名）**：**CoCo**（原 Cortex Code，AI 编码 agent，9,100+ 账户）；**CoWork**（原 Snowflake Intelligence，业务人员 agent，5,800+ 账户）；底层 Cortex AI（AISQL / Analyst / Search / Agents）；**Cortex AI Gateway**（2026-07-28，统一管 agent→模型/工具/MCP，2026-08-18 加 dynamic model routing）。
- **人**：CEO **Sridhar Ramaswamy**（2024-02 起；Chairman Frank Slootman）；EVP Product Christian Kleinerman；SVP Eng Vivek Raghunathan；CTO S. Muralidhar。员工 ≈ 9,400。
- **地**：SEC 总部 Bozeman；最大工程园区 **Menlo Park**；**Bellevue** Spring District（2026-06 又扩 3 层）。Database Engineering 团队分布 Menlo Park / Bellevue / Berlin。
- **战略三句**：① AI 控制平面（三重飞轮：AI 工作负载 → CoCo/CoWork 采用 → 消耗更多算力）；② 消费模型 + 模型中立（Anthropic $200M、OpenAI $200M 合作；"competing with Anthropic on LLM quality is not a winning strategy"）；③ 开放互操作（Iceberg v3、Apache Polaris 2026-02 成为 Apache 顶级项目）+ 往 OLTP 上移（Unistore、**Snowflake Postgres** 2026-02-24 GA）。
- **近期事故**：2026-09-09 21:26–21:55 UTC 部分元数据基础设施不可用（status 页公开）—— 反问素材。

## 1. 必会架构词（大白话，能 30 秒讲清）

| 词 | 一句话 | 为什么面试会碰到 |
|---|---|---|
| **三层架构** | 数据以不可变列式 **micro-partition** 存对象存储；**virtual warehouse** 是独立计算集群，按秒计费；**Cloud Services（内部 GS）** 无状态服务做认证 / 元数据 / 优化 / 事务，元数据全在 **FoundationDB** | 所有特性的根：clone、time travel、多仓库并发都靠「数据不可变 + 元数据集中」 |
| **Zero-copy clone / Time Travel** | clone 只复制元数据指针；表版本历史在 FDB，所以能 `AT(TIMESTAMP)` / `UNDROP`（默认 1 天，最长 90 天） | 我用 clone 做过隔离 schema pool（S7） |
| **Result cache** | 同 SQL + 数据没变 → 24 h 内直接返回，不起仓库 | 成本题 |
| **Streams** | 一个 offset 书签指向表版本；查 stream 得净变化 + `METADATA$ACTION/ISUPDATE/ROW_ID`；**只有在 DML 事务里消费才推进 offset**；类型 standard / append-only / insert-only | 我的 AMEX 管线用了 6 条 append-only stream |
| **Tasks** | CRON / 间隔 / DAG；`WHEN SYSTEM$STREAM_HAS_DATA()` 避免空跑；serverless 或自管仓库；`SUSPEND_TASK_AFTER_NUM_FAILURES`、`TASK_HISTORY()` | 我的整条编排 |
| **Dynamic Tables** | 把「stream + task + MERGE」声明化：`TARGET_LAG`，自动推依赖图、增量/全量；2026-07 加 Adaptive Refresh | 「如果重来我会用它」的候选答案 |
| **Snowpipe / Snowpipe Streaming** | 文件事件触发微批 vs 行级 channel + offset token exactly-once，单表 10 GB/s、5 s 延迟 | ingestion 话题 |
| **Datastream**（Summit 2026 预览） | Snowflake 原生、**Kafka wire-compatible** 流服务，topic 直接落表并继承 RBAC / lineage / Time Travel | 我 intern 做过 Kafka→Snowflake connector |
| **Unistore / Hybrid Tables** | 行存主表 + 强制 PK + 行锁，毫秒点查；后台异步同步到列存；事务引擎是 FDB | 「结算类 OLTP 该放哪」 |
| **Iceberg / Polaris / Horizon** | 开放表格式 + 开源 REST catalog（Apache TLP）+ 治理统一层（AI Agent Identity GA） | 开放战略 |
| **Snowflake Postgres** | 真 Postgres 实例（Crunchy Data，~$250M，2025-06 收购），零改代码，2026-02-24 GA | 我在 PayPal 用 PostgreSQL 做 pricing OLTP |
| **Execution Anchor**（工程博客 2026-05-05） | 每个查询绑定恰好一个 GS 实例，绑定存 FDB；~99% 查询不转移；崩溃时两阶段非自愿转移 | **分布式协调 / exactly-one-writer 的最佳谈资** |

## 2. 工程文化（公开可说）

- **栈**：执行引擎 XP 用 C++（GC 停顿不可接受），控制面 GS 用 Java；三云同一代码库；SLA 99.9%，2022 起 99.99% 目标；严格 postmortem + 对外 RCA。
- **计量与计费**：credits 按秒（仓库 60 s 起）；Cloud Services 每日免费额度 = 仓库消耗 10%；serverless 各有费率；AI 按 token（`METERING_HISTORY.SERVICE_TYPE='AI_SERVICES'`），2026-03 起 AI 花费上限、2026-07 per-user 配额 → **我的「金融级对账」经验直接映射到「计量级对账」**。
- **AI-native 工程**：SVP Eng 博客（2026-08-05）"treat your developers like customers"；CEO："a tech lead of agents rather than an IC that writes code one line at a time"；与 Anthropic 合作条款里明确内部用 **Claude Code** → 我简历第 4 条 bullet（AI-native workflow）正好对上。
- **Observe 收购**（2026-02 完成，~$596M）→ 可观测性内化；Menlo Park 有 Observe 后端岗。
- **风险提示（Blind/Glassdoor，匿名）**：工程师 WLB 2.9/5（Menlo Park 2.4 / Bellevue 3.3）；RTO 3 天/周 + badge 追踪；on-call 看团队；2026-03 裁约 70 人（文档团队）。→ team matching 时问 pager 频率与 RTO 执行。

## 3. 八条价值观（2026-02-23 Code of Conduct 原文关键词）

| 值 | 关键词 | 我的故事 |
|---|---|---|
| Put Customers First | earn trust · listen · pain points | S4（PM escalate → 给所有人同一份证据）· S9（DoorDash SLA） |
| Integrity Always | speak up candidly · disagree then **commit fully** | S6（写 go/no-go 叫停）· S2（自曝设计缺陷写 ADR） |
| Think Big | ambitious · prudent risks | S5（$55B TPV 前提）· Quant-Stroller 66K 行 |
| Be Excellent | quality · simplicity · today and tomorrow | S5 shadow-run 0.224% · S2 框架复用 8 次 |
| Get It Done | results · precise yet nimble · follow through | S8（7 分钟 RCA 出 PR）· S1 18 个月生产 |
| Own It | like it's yours · own issues · own mistakes | S3（自己转发 pager 当场根因）· S2（自己修自己的缺陷） |
| Make Each Other the Best | help · feedback · teach | Ziyang domain-ownership 框定 · onboarding doc 维护两年 |
| Embrace Differences | different experience | 跨 Pricing / Funding / Fiserv 三方对齐（S5）；跨时区 Chicago→San Jose |

## 4. 近 90 天可引用的事（按日期）

- 09-09 元数据基础设施事故（29 min）· 09-08 Goldman 会议：CEO 承认「迁入快 = 迁出也快」，要 move upstream · 09-02 财报 · 08-18 dynamic model routing · 07-28 Cortex AI Gateway（Black Hat）· 07-21 Dynamic Table Adaptive Refresh、Managed Agents GA · 06-03 Natoma 收购完成（MCP 网关 → Gateway 基础）· 06-01~04 Summit 26（CoCo/CoWork 改名、Cortex Sense、Datastream、Iceberg v3、Openflow 三云 GA）· 05-27 AWS $6B/5 年承诺。

## 5. 我与 Snowflake 的五座桥（Why Snowflake 的骨架）

> 定位一句：**"I'm one of Snowflake's heaviest kinds of user — I run a transactional financial system on it. I've hit every consistency and scheduling edge, and I'd rather fix them than route around them."**

| 我做过（用户侧） | 对应内部系统 / 团队 | 能展开的话题 |
|---|---|---|
| Streams + MERGE 做 CDC 与幂等对账 | GS 事务 / 元数据层（FDB）；Dynamic Tables | 表版本与 MVCC、stream staleness、增量刷新何时退化成全量、exactly-once |
| Tasks DAG + feature-flag 调度、失败重试、`TASK_HISTORY` 监控 | Serverless Tasks / 调度器；Adaptive Refresh | 调度器 leader 选举、`STREAM_HAS_DATA` 触发、DAG 部分失败语义、serverless vs warehouse 计费 |
| 结算 / 手续费分毫不差 + 自建 quality-check 框架 | **Metering & billing**（credits、AI token 计量、花费上限） | 计量管道的幂等 / 迟到数据 / usage→invoice 对账；多模型路由后成本归因 |
| Terraform 管 grants / RBAC、clone 做环境隔离 | Horizon / 治理与安全（AI Agent Identity、Trust Center） | RBAC 在 FDB 里的表达与缓存、权限传播一致性、审计写放大 |
| UDTF / stored proc 承载业务逻辑 | Query Processing（C++ XP + Java GS）、Unistore/FDB、Snowflake Postgres | UDTF 边界开销、沙箱隔离、结算 OLTP 放 Hybrid Table 还是 Postgres（我有真实负载可比） |

额外：query-history 驱动的质量检查 → Observe；支付事件流 → Snowpipe Streaming / Datastream（intern 做过 Kafka→Snowflake connector）。
