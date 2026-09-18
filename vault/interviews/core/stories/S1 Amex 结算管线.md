---
title: S1 · Amex 结算管线
aliases:
  - S1
  - Amex 结算管线
  - AMEX GRRCN
tags:
  - interview/story
  - stack/snowflake
  - stack/sql
  - stack/distributed-systems
  - stack/production
answers: [Q1, Q18, Q22]
stacks: [TS03, TS07, TS10]
status: verified
---

# S1 · Amex 结算管线（旗舰：端到端 ownership）

> [!abstract] 一句话
> 我从一个 stub 起，设计并建成了 Braintree 的 American Express 结算文件管线——Snowflake-native 的 `COPY INTO` → 六条 append-only Stream → 复合键 `MERGE` → 校验 UDTF → 费用计算 Task——并做了 18 个月的生产防御与 EU 扩展；它一年处理数千万笔 Amex 交易、数十亿美元。

## 1. 背景：为什么 Amex 不能乐观入账

Visa / Mastercard 走收单行（Fiserv）的准实时 settle / tran 视图；**Amex 是闭环网络**，每天甩一个**专有定宽文件**（GRRCN，Global Reconciliation Report & Chargeback Notification）过来，里面混着交易、定价、调整、拒付、费收入、汇总六种记录类型。所以 Amex 交易到达时不能直接进 `TRANSACTIONS`，必须先趴在 `PENDING_TRANSACTIONS`，等文件验真后再"转正"——这就是 **good-funds model**。管线的输出喂给费用计算和出款（Funding）。

## 2. 机制（说得出原语名）

```
S3 文件 ──COPY INTO──▶ 一行一记录的 staging 表（行首 10 字符切出 RECORD_TYPE）
                          │  六条 APPEND_ONLY Stream，各自独立 offset
                          ▼
             六个 procedure：SUBSTRING 按偏移切字段 → MERGE 进六张类型化表
                          │  复合键 = 参考号 + 拒付指示位（EQUAL_NULL）
                          ▼
             两个 UDTF（RETURNS TABLE）：FULL OUTER JOIN pending ↔ 文件记录
                          │  匹配 → 迁入 TRANSACTIONS；不匹配 → ERROR_LOGS，永不丢
                          ▼
             费用计算 Task：AFTER A, B（双上游）+ WHEN SYSTEM$STREAM_HAS_DATA
                          │  BEGIN TRANSACTION { 算费; 记错误日志 } COMMIT
                          ▼
             聚合 → Funding 出款
```

关键设计决定与取舍：

| 决定 | 为什么 | 代价 / 怎么兜 |
|---|---|---|
| append-only Stream × 6 而不是一条标准 Stream | 每种记录类型独立 offset，互不阻塞；语义退化成"游标前进" | Stream 的 offset 推进和业务写入不是一个事务——正确性靠下游 `MERGE` 键，不靠 Stream |
| 幂等三层：`COPY INTO` 文件级去重（`FORCE=FALSE` + load history）· 每级 `MERGE` 键 · 校验 UDTF 记错不丢 | 文件会重投、Task 会重跑；结算数据宁可重跑也不做"一次跑对"的乐观假设 | 复合键允许同一参考号的"正常"与"拒付"两条并存，由校验决定取舍 |
| 一个 feature flag 把 Amex 摘成独立流 | 不动其他卡网络的乐观入账路径；一条 `UPDATE` 即急停，不发版 | 多开关叠加（EU 又一个）要人工核对环境间一致性 |
| `PATTERN` 正则扫全部日期目录 | 事故教训：文件落进"昨天"目录时今天已经翻页，按日期过滤会漏 | 迟到文件下次跑被捡起，但那几天的下游已经出过一版少数据的结果 |
| `AFTER A, B` 双上游 + FULL OUTER JOIN 兜底 | `AFTER` 只保证两边各跑过一次，不保证同一批；错位的记录记一次错误、下一轮自愈 | 错误日志里有"下一轮就消失"的噪音，runbook 要区分 |
| 定长解析写在 procedure 的 `SUBSTRING` 里，不是设计文档里说的 UDTF | 省一层调用；两个真正的 UDTF 用于校验 | 六份偏移表重复六次——**我会改**：偏移配置表 + 一个通用解析 UDTF |
| `TRY_TO_DECIMAL` / `TRY_TO_DATE`，隐含小数 `/10000`、`/100000` | 一个坏字符不该炸掉整批 | 坏值变 NULL 而非异常，要靠校验层抓 |

## 3. 我做了什么

接手时只有前任留下的一张表的 stub。从设计文档起：拓扑、六个解析 procedure、两个校验 UDTF、费用计算 Task、急停开关、EU 扩展（第二个 flag + `european_amex_interchange` 独立账目）、约十几个加固 PR（迟到文件、拒付标志、大小写、错误日志处理）、Streamlit 任务监控 + Datadog 告警。任期内最大的单个 PR（约 1,800 行）就是这条管线。

## 4. 量级与口径

| 数字 | 口径 | 状态 |
|---|---|---|
| ~22M 笔 Amex 交易 | 生产 `TRANSACTIONS` 里 `sub_kind = american_express`，2025-05-20 起半年 | ✅ 出处确凿 |
| "billions of dollars" | 同一查询的 `SUM(amount)`——页首注明**以分计**，故 $138.6B 很可能是 **$1.386B**（每笔 ≈ $63，Amex 费 ≈ $1.84/笔，算术吻合） | ⚠️ 口播只说量级 |
| 18 个月生产 | 2025-04 首个 PR 合并至今 | ✅ |
| ~1,800 行 | 最大单 PR，API 精确核对 | ✅ |

> [!warning] 证据边界
> - **不说** "top committer / 615 commits"（GitHub 口径 66 commits、第 15）；说 "~90 PRs，仓库里两个最大的改动是我的"。
> - **不说** "我把 Funding 的 Ruby 脚本迁到 SQL"（funding 仓库零足迹）；说 "Amex 结算逻辑原来在 Rails 出款服务里，我的管线是接收侧的 Snowflake-native 替代"。
> - **不说** "no bugs, no accidents"——[[S3]] 就在这条线的下游；说 "坏了的时候管线记下来而不是丢掉，这是我最自豪的设计"。
> - **不说** "parsing UDTFs"；说 SUBSTRING in procedures + two validation UDTFs（设计文档与代码的出入本身是好素材）。

## 5. English · 首答（90 s）

> The project I'd pick is the American Express settlement pipeline on our Snowflake-native fee platform. Amex is a closed-loop network: instead of the near-real-time settlement views we get from our acquirer for Visa and Mastercard, Amex sends one proprietary **fixed-width reconciliation file** a day. That means we can't optimistically book an Amex transaction — it has to sit in a pending table until the file confirms it settled, which is our **good-funds model**.
>
> I owned the pipeline end to end, from the design document to eighteen months of production hardening. Mechanically: a scheduled Snowflake **Task** runs `COPY INTO` from S3 into a staging table, one line per row; six **append-only Streams** fan those rows out by record type; six stored procedures parse the fixed-width fields with offset-based `SUBSTRING` and `MERGE` them into typed tables on a composite key; two table functions validate the parsed records against the pending transactions with a `FULL OUTER JOIN` so that every mismatch lands in an error log instead of being dropped; and a downstream Task with **two upstream dependencies** computes the interchange fee per transaction inside one explicit transaction, then hands aggregates to our payout service.
>
> The design decisions I'd highlight: append-only streams so each record type has an independent offset and consumers don't block each other; `COPY INTO`'s file-level dedup plus composite-key `MERGE` at every stage, so retries and re-ingested files are idempotent; and a single feature flag that routes Amex into this separate flow without touching the code path every other card network uses. Later I extended it to the EU aggregator flow with a second flag and a different fee ledger.
>
> It's been processing tens of millions of transactions a year — billions of dollars — and it's the reference implementation the team points to for "how do we onboard a new file-based settlement source."

## 6. English · 追问版（每条 ≤ 45 s）

- **What was specifically yours?** → "I inherited a stub with one table. Everything from the topology onward is mine — the staging and stream design, the six parsers, the validation table functions, the fee-calculation task, the kill switch, the EU extension, and about a dozen hardening PRs. The largest single PR in my tenure — around 1,800 lines — is this pipeline. I also wrote the design doc the team reviewed."
- **Why Streams and Tasks instead of Airflow or Spark?** → "Data locality and transactional semantics. The file lands in Snowflake anyway; keeping parse-validate-compute inside the warehouse means every step is a `MERGE` inside a transaction and nothing leaves the account. `SYSTEM$STREAM_HAS_DATA` gates each task so we never spin up a warehouse on empty input. The trade-off is orchestration is weaker than Airflow — no branching, no external callbacks — so I built the observability on top: a Streamlit task monitor and Datadog alerts driven by health-check procedures."
- **How do you know it's correct?** → "Three layers. Row level: `TRY_TO_DECIMAL` and `TRY_TO_DATE` so a bad field never aborts the batch, and rejected records are kept, not dropped. Batch level: health checks assert every settled transaction has its fee. Reconciliation level: fee totals reconcile against the summary record type Amex itself sends. A mismatch halts the task and pages the on-call — which has been me."
- **What broke?** → "Two things worth telling. First, file timing: Amex would drop a file into yesterday's date folder after we'd moved on to today. I changed the ingestion to scan every date partition with a `PATTERN` regex and rely on `COPY INTO`'s load history for dedup. Second, the reject flag: a transaction can appear once as settled and later as rejected; I made the `MERGE` key composite — reference number plus reject indicator — so both states coexist and the validator decides which one wins."
- **What would you change?** → "The six parsers repeat the same offset table six times. I'd move field offsets into a config table and write one generic fixed-width parsing UDTF — adding a seventh record type becomes a config row, not a new procedure. That's exactly the pattern I used later in the quality-check framework."
- **How does this relate to what Snowflake builds?** → "I've been a very heavy consumer of Streams, Tasks, `MERGE` semantics, task DAG dependencies and warehouse cost controls for two years. I know where they're great and where they hurt — stream staleness is silent, task-level observability is thin — and that's the platform side I want to work on."

## 7. 用在哪

- 回答：[[Answers#Q1]] 最难项目 · [[Answers#Q18]] 端到端 owner · [[Answers#Q22]] 优势
- 场景题：计量不重复计费 · 调度器 DAG · 迟到数据（[[scenarios|Chakra scenarios]] §2 §10 §12）
- 技术栈：[[03-snowflake-warehouse|TS03 Snowflake]] · [[07-data-pipelines-cdc|TS07 数据管道与 CDC]] · [[10-correctness-idempotency|TS10 分布式正确性]]
- 相邻故事：[[S3]]（这条线下游的事故）· [[S2]]（这条线用到的质量门禁）· [[S9]]（这条线的出款延迟事故）

## 8. 证据锚点

PR #751 / #856 / #862 / #886（1,849 行）/ #911 / #1023 / #1988 / #2598；设计文档 Confluence 2233926829；Impact Summary 2750481503；代码级拆解见本机 `raw/code/01-amex-grrcn-pipeline.md`（gitignore）。
