---
title: S2 · Quality-check 与 trigger-status 框架
aliases:
  - S2
  - Quality-check 框架
  - Trigger-status handshake
tags:
  - interview/story
  - stack/snowflake
  - stack/sql
  - stack/distributed-systems
answers: [Q2, Q4, Q11, Q12, Q16, Q19, Q24]
stacks: [TS03, TS08, TS09]
status: partial
---

# S2 · Quality-check 与 trigger-status 框架（平台化：别人往上接）

> [!abstract] 一句话
> 我把"每张对账表各写一个校验 task"收敛成一个**配置驱动**的质量门禁框架 + 一个"数据可读"的握手信号，自己铺开八个 subject area；之后发现自己设计的粒度缺陷（50 个坏商户挡住 35,000 个），写了正式 ADR 把 readiness 降到商户级。

## 1. 机制

| 层 | 是什么 | 关键写法 |
|---|---|---|
| 配置 | `QUALITY_CHECK_CONTRACT_CONFIG`：一行 = (subject area, validation) → 校验 procedure 名、日期列、SLA 小时、JSON 参数、是否启用 | 加一条校验 = `INSERT` 一行，不发版 |
| 执行 | `EXECUTE_QUALITY_CHECK`：`EXECUTE IMMEDIATE` 拼 `CALL <proc>(…)`，`RESULT_SCAN(LAST_QUERY_ID())` 取回结果，归一成 PASS / FAIL / WARNING 写结果表；`EXCEPTION WHEN OTHER` 把崩溃转成一条 FAIL 记录 | 新旧返回格式双兼容，老校验可增量迁移 |
| 握手 | `POPULATE_TRIGGER_STATUS`：某 subject area 当日所有启用校验最新结果都 PASS → `TRIGGER_STATUS = Completed`；该行复制到 share 层 | 下游 `JOIN … WHERE STATUS = 'Completed'`——**"能不能读"从 Slack 约定变成 SQL 里的硬条件**（[[S5]] 就是消费者） |
| SLA | 07:00 PT 前所有 subject area 必须 Completed，否则告警 | 握手解决时序，校验解决内容——两者互补不替代 |

取舍：`EXECUTE IMMEDIATE` 动态 SQL 失去静态检查（配置写错要到运行时才知道），且要求配置是内部可信输入；`EXCEPTION WHEN OTHER` 把异常压成字符串，排查靠读文本。

## 2. ADR：从表级阻塞到商户级

问题：readiness 是 subject-area 级——一个商户的数据坏了，整张表对所有商户不可读；生产数据里约 50 个持续失败的商户（~4%）挡住 35,000 个。

四方案对比（ADR 原文的核心论证）：

| 方案 | 读侧代价 | 结论 |
|---|---|---|
| A · VARIANT 列 + 逐行 UDF | secure view 遇到逐行 UDF / VARIANT 解析会**关闭谓词下推**，五千万行的表不能这么跑 | 否 |
| B · VARIANT + FLATTEN 中间视图 | 可接受，但 VARIANT 有 16 MB/cell 上限（~98K 商户） | 否 |
| C · 新建逐商户失败表 | 最优 JOIN，但要加表 + Iceberg 同步 stream/task | 否 |
| **D · 复用结果表，摊平成"汇总行 + 逐商户失败行"** | flat 列等值 JOIN，零新增基础设施；已有一个 subject area 这样跑了 16 个月 | **选中** |

正确性论证——**strictest wins**：读查询先判 `NOT EXISTS (表级失败)` 再判 `NOT EXISTS (商户级失败)`，所以改造过与未改造的 procedure 混跑永远安全（未改造的退化成表级阻塞 = 今天的行为）。容量论证：96.4% 的检查一次通过、失败是稀有事件，所以只存失败行（"PASS 行语义为空"），极端情况每月 ~80 万行，微不足道；反之"每商户每次都写一行"是每天 240 万行。

## 3. 量级与口径

框架 PR 约 1,500 行；铺开 8 个 subject area（各 200–800 行）；ADR 影响面 35,000 商户 / ~50 坏商户。

> [!warning] 证据边界
> ADR 状态是 **Proposed**，`HAS_MERCHANT_DETAIL` 不在代码里；商户级模式只在一个 subject area（TRANSFERS）有 16 个月先例。
> **说法**："The framework and eight rollouts are live; merchant-level readiness is designed, reviewed, and proven for one subject area, and the framework-wide rollout is sequenced behind the net-settlement ramp." **不说** "改成了 / 上线后效果是…"。

## 4. English · 首答（90 s）

> The team had dozens of reconciliation tables — acquirer settlement, adjustments, tax, transaction reconciliation — and every new one got its own hand-written validation task. I replaced that with a **config-driven quality-check framework** that the whole team now onboards onto.
>
> Three pieces. A contract-config table: one row per (subject area, validation) that names the stored procedure to run, the date column, an SLA in hours and a JSON parameter blob. A generic executor that reads the config, builds the call with `EXECUTE IMMEDIATE`, captures the result through `RESULT_SCAN`, and writes a normalized PASS / FAIL / WARNING row — with an exception handler so one broken check never takes down the others. And a **trigger-status state machine**: when every enabled check for a subject area passes, the status flips to `Completed`, and that row is replicated to a share layer where downstream consumers `JOIN` on it. So "is this data safe to read" stopped being a Slack convention and became a `JOIN` condition in the consumer's SQL.
>
> Adding a check went from "write a new task, get it reviewed, deploy" to "insert a config row." I rolled it across about eight subject areas myself, and it's the mechanism my later interchange-source migration used to know the upstream settlement view was ready.
>
> The follow-on I'm proudest of is a design I drove after seeing a flaw in my own first version: readiness was per table, so roughly fifty bad merchants out of thirty-five thousand could block everyone. I wrote a formal ADR — four alternatives, a correctness argument that the table-level block always wins over merchant-level, and a volume analysis showing failures are the rare case so a sparse "one row per failing merchant" model costs almost nothing. That's the direction the team is taking the framework.

## 5. English · 追问版

- **Why dynamic SQL — isn't that risky?** → "It's the price of config-driven. The config is engineer-controlled through migrations, not user input, so injection isn't the threat model; the real cost is losing static checking — a typo in a config row fails at runtime. I mitigated that with the exception handler and a health check on the results table itself."
- **Why a status table instead of task dependencies?** → "The consumers are in different databases, sometimes different accounts. A replicated status row is the lowest-common-denominator contract that crosses those boundaries; task `AFTER` dependencies don't."
- **Correctness argument?** → "Strictest wins. The read query checks `NOT EXISTS (table-level failure)` before `NOT EXISTS (merchant-level failure)`, so a mixed deployment is always safe: an unrefactored procedure degrades to blocking everyone, which is today's behavior."
- **Why not VARIANT?** → "A secure view over a per-row UDF or VARIANT parse disables predicate pushdown, and I wasn't going to run that over tens of millions of rows; and VARIANT has a per-cell size ceiling a large merchant list can hit. Flat relational rows with an equality join keep pruning intact."
- **Status?** → "Framework and eight rollouts in production; merchant-level designed, reviewed, proven for one subject area, sequenced behind the net-settlement ramp."

## 6. 用在哪

- 回答：[[Answers#Q2]] 架构决策 · [[Answers#Q4]] 系统设计贡献 · [[Answers#Q11]] 定标准 · [[Answers#Q12]] 说服团队 · [[Answers#Q16]] 传递工程标准 · [[Answers#Q19]] 失败与成长 · [[Answers#Q24]] 接受批评
- 场景题：下游永不读到半成品数据 · 一个坏租户挡住所有人
- 技术栈：[[03-snowflake-warehouse|TS03]] · [[08-observability-oncall|TS08]] · [[09-sql-data-modeling|TS09]]
- 相邻：[[S5]]（消费这个握手）· [[S7]]（同样"造工具给别人用"）

## 8. 证据锚点

PR #1997（+1489）+ 铺开 #2061 / #2069 / #2075 / #2091 / #2106 / #2558 / #3040 / #3237；ADR Confluence 2894288991（Proposed）；代码级拆解见本机 `raw/code/02-quality-check-framework.md`。
