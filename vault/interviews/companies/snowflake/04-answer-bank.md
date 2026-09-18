---
title: Snowflake answer bank
aliases:
  - Snowflake answer bank
tags:
  - company/snowflake
---

# 04 · 答案库（题 → 既有答案映射 + Snowflake 特定题）

> 通用题不重写：指向 [[Answers]] 的 Q 号（中文详版，A 影响导向 / B 技术展开）。本文件补三样：① Chakra 四段最可能的题及英文首答要点；② Snowflake 特定题；③ 8 条价值观 × 故事矩阵。英文口述稿以故事笔记（[[Core]] → [[S1]]…[[S11]]）与 `loop/rounds/00_ai_screen/playbook.md` 为准；完整题库（79 题）在 `loop/rounds/00_ai_screen/questions.md`。这里保留 Snowflake 特定题、价值观矩阵和数字卡。

## 1. 段一 · Experience & role-related background

| 题（英文） | 映射 | 英文首答要点（headline → mechanism → number → learning） |
|---|---|---|
| Tell me about yourself / your current role | `fit.md` · `loop/rounds/00_ai_screen/playbook.md` §2 | 见 playbook §2，60 s |
| Walk me through a recent project and your specific contribution | [[Answers#Q1]] · [[Answers#Q18]] → **[[S1]]** | stories §[[S1]] |
| What's the hardest technical challenge you've faced? | [[Answers#Q3]] → **[[S3]]** | ACH NULL-concat RCA：196 merchants / $11.3M/day；UDF overload；non-null assertion added |
| What's a project you're most proud of? | [[Answers#Q5]] → **[[S5]]** | Net settlement：$450M/mo float → T+1；shadow-run 13.7M rows / 0.224%；$55B TPV prerequisite |
| Tell me about something you built that others reuse | [[Answers#Q4]] · [[Answers#Q11]] → **[[S2]]** | Quality-check framework：config-table driven + handshake；reused ~8×；ADR fixed my own flaw |
| What did you do as an intern? | [[S11]] | Kotlin/Spring fee service；Kafka→Snowflake connector with protobuf converter + poison-message isolation；Airflow DAGs scheduling Spark validators |
| Tell me about a side project | Quant-Stroller | 66K lines / 470 test files；dual-gate anti-overfitting；DuckDB point-in-time data plane；8-GPU self-hosted CI — 只在被问时讲，≤ 45 s |
| How do you use AI tools in your work? | 简历 bullet 4 · [[S7]] | Claude Code for review/test-gen/refactor in the Ruby→Snowflake migration；built snowglobe-tools schema pool so multiple agent sessions run in parallel without DDL collisions；**"tech lead of agents"** 呼应 CEO 原话 |

## 2. 段二 · Applied scenarios → `loop/rounds/00_ai_screen/scenarios.md`（12 题）

## 3. 段三 · Collaboration & decision-making

| 题（英文） | 映射 | 要点 |
|---|---|---|
| Describe a technical decision and the trade-offs | [[Answers#Q2]] → **[[S5]]** | shadow-run vs flip-and-monitor；2 extra weeks vs zero fee regression |
| A time you disagreed with a teammate / another team | [[Answers#Q14]] → **[[S4]]** | PM escalation, 50-reply thread；gave everyone the same query；AU `fee_refund_policy='partial'`；USA 1,079,627 rows vs AUS 0 |
| A time you pushed back / said no | [[Answers#Q20]] → **[[S6]]** | go/no-go gate；QA 834M rows/6 merchants vs prod 39B/18,140；760M rows/day serving would OOM；froze CI/CD until gate |
| A time you convinced the team to change approach | [[Answers#Q12]] → **[[S2]]** | ADR with 3 rejected alternatives；merchant-level granularity |
| Cross-team project you drove | [[Answers#Q10]] → **[[S5]]** | Pricing / Funding / Fiserv alignment；epic chain over 2 years |
| A mistake you made and what you changed | [[Answers#Q19]] · [[Answers#Q24]] → **[[S2]]** | my framework's 4%-blocks-all flaw；wrote the ADR myself；now every check has a granularity decision up front |
| How do you prioritize when everything is urgent? | [[Answers#Q20]] | revenue-impacting correctness first；then unblocking others ([[S8]] 7-min RCA)；then roadmap；say what slips before it slips |
| Helping a teammate grow | [[Answers#Q13]] · [[Answers#Q15]] | Ziyang：domain-ownership framing — his exclusion service and gRPC journaling sync integrate into my domain; I define contracts and am the fee-calc authority in incidents. **不编 1:1 细节**；onboarding doc maintained 2024→2026 |
| Working with someone very different from you | [[Answers#Q14]] · Embrace Differences | 跨 Pricing(Kotlin) / Funding(Ruby) / Fiserv(external) 的语言与节奏差异；Chicago intern → San Jose |
| A time you delivered bad news | Integrity Always → **[[S6]]** | told the org the intern's detector wasn't prod-ready；wrote it down with numbers |

## 4. Snowflake 特定题（English）

**"Why Snowflake?" / "What do you know about Snowflake?" / "Why leave PayPal?"** → `fit.md`

**"You've used Snowflake heavily — what would you change about it?"**（Put Customers First 反向题，很可能被问）
> Two things, both from running a financial workload on it. First, observability of Streams and Tasks: when a task in a DAG fails, `TASK_HISTORY` tells me it failed, but the path from "which upstream row caused it" is manual — I ended up building a Streamlit monitor and Datadog alerts on top. Second, stream staleness is silent: if a consumer doesn't advance the offset inside a DML transaction, you find out later. I'd love a first-class "this stream is about to go stale" signal. Dynamic Tables solve part of this declaratively, which is exactly why I find that team interesting.

**"Streams vs Dynamic Tables — when would you use which?"**
> Streams and Tasks when I need imperative control — a MERGE with custom conflict logic, a feature flag mid-DAG, a call-out to a stored procedure. Dynamic Tables when the transformation is a pure SELECT and what I care about is a target lag: the engine picks incremental vs full refresh and handles the dependency graph. For my fee pipeline the parsing and MERGE stages stay as tasks; the downstream aggregates could be dynamic tables today.

**"How does Snowflake's architecture make zero-copy cloning possible?"**
> Micro-partitions are immutable and a table is just a versioned list of partitions in metadata — in FoundationDB. A clone copies that list, not the data; both tables then write their own new partitions. Same mechanism gives Time Travel: the old version's list still exists until retention expires.

**"What's the difference between a warehouse and cloud services in terms of cost?"**
> Warehouses bill credits per second with a 60-second minimum while running; cloud services — parsing, optimization, metadata — are free up to 10% of daily warehouse consumption and billed beyond that. Serverless features like tasks and Snowpipe have their own rates. As a user I tuned this: `STREAM_HAS_DATA` gating so tasks don't spin up warehouses on empty input.

**"Tell me about a time you put the customer first when it was inconvenient."**
> The AU refund-fee issue ([[S4]]): the fastest close was "not my team's config." Instead I pulled the data — a million US rows vs zero AU — wrote the query so the PM could verify it herself, and it became a tracked fix. Inconvenient because it wasn't on my board that week; right because merchants were being under-charged silently.

## 5. 价值观 × 故事矩阵（每条至少一个故事，追问时切换）

| 值 | 主故事 | 备用 | 一句证据 |
|---|---|---|---|
| Put Customers First | [[S4]] | [[S9]] | "gave the PM the query so she could verify it herself" |
| Integrity Always | [[S6]] | [[S2]] | "wrote down that the detector wasn't prod-ready, with the numbers" |
| Think Big | [[S5]] | Quant-Stroller | "the prerequisite for ~$55B of incremental volume" |
| Be Excellent | [[S5]] shadow-run | [[S1]] | "0.224% variance, every category explained, before we switched" |
| Get It Done | [[S8]] | [[S1]] | "seven minutes from alert to PR; release shipped" |
| Own It | [[S3]] | [[S2]] | "I forwarded the page to myself and posted the root cause" |
| Make Each Other the Best | Ziyang（domain framing） | onboarding doc | "his work integrates into the domain I own; I define the contracts" |
| Embrace Each Other's Differences | [[S5]] 三方 | intern 跨城 | "three teams, three languages, one reconciliation" |

## 6. 数字卡（只说这些）

| 数字                                                       | 属于            | 说法                                                            |
| -------------------------------------------------------- | ------------- | ------------------------------------------------------------- |
| 21.96M txns / $138.6B                                    | [[S1]]（2025 Amex） | "about 22 million transactions, 138 billion dollars, in 2025" |
| 18 months in prod                                        | [[S1]]            |                                                               |
| ~8 reuses                                                | [[S2]]            |                                                               |
| 196 merchants / $11.3M/day / 1.05M rows                  | [[S3]]            |                                                               |
| 1,079,627 vs 0 / 157 merchants                           | [[S4]]            |                                                               |
| $55B+ TPV / $450M/mo float / 13.7M rows / 0.224%         | [[S5]]            |                                                               |
| 834M vs 39B rows / 6 vs 18,140 merchants / 760M rows/day | [[S6]]            |                                                               |
| 7 minutes                                                | [[S8]]            |                                                               |
| ~90 PRs / two largest changes in the repo are mine       | 画像            | "measured by what the pipelines process, not commit count"   |
| **不说**：$600B                                             | 简历口径未闭合       | 被问时按 playbook §7                                              |
