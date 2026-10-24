# 项目深挖演练（两个旗舰项目）

- 简历拷问和 HM 面会拿一个项目问 30 分钟：为什么选这个技术、规模数字、取舍、重来改什么、哪里会坏。下面是你最强的两个项目，各 13 个问题，每题给答案提纲。
- 项目 A：Amex 结算管线（[[S1_settlement-pipeline-never-drop-bad-data|S1]]）。项目 B：interchange 数据源切换（[[S5_cutover-with-the-production-query|S5]]）。
- 用法：把 13 个问题连着问自己，每题 45–90 秒；每周一次计时，整套 30 分钟。
- 对抗式追问的三招：
  - 有两个选项时，先说**各自的代价**，再选一个，**之后不改口**。
  - 被问到没测过的东西，说**最深已知层 → 边界 → 怎么查**。
  - 数字只用这页有的；规模换算要说明是**算出来的**。

## 项目 A · Amex 结算管线（S1）

### A1 · 30 秒讲清楚这个项目
- **Context**: Amex is **closed-loop**: one **fixed-width file a day**; we can't book a transaction until the file **confirms** it settled (the **good-funds model**).
- **Mine**: I inherited a **stub with one table** and owned the pipeline **end to end**, design doc to **18 months** of production.
- **Result**: about **22M transactions** in half a year; the team uses it as the reference for onboarding a **file-based settlement source**.

### A2 · 为什么用这套技术（Snowflake Streams / Tasks），不用 Airflow、Spark 或 Kafka？
- **Data locality**: the file lands in Snowflake anyway; parse, validate and compute **inside the warehouse**, nothing leaves the account.
- **Transactions**: each step is a `MERGE` in a **transaction**; `SYSTEM$STREAM_HAS_DATA` gates each task so no warehouse **spins up on empty input**.
- **Cost**: **weaker orchestration** (no branching, no external callbacks), so I built **monitoring on top**: a task monitor and **Datadog** alerts.
- **Why not Kafka**: the source is a **daily file**, not a stream; a log would add moving parts with no benefit.
- **Follow-up: would Airflow have been better?** For branching and callbacks, yes; for **transactional steps next to the data**, no. 【待补：当时设计评审里的反对意见】

### A3 · 规模数字是多少？这算大吗？
- **Numbers**: ~**22M transactions** in half a year; **18 months** in production; largest single PR ~**1,800 lines**.
- **Derived**: about **120K transactions a day**, ~**1.4 per second** on average (22M ÷ ~183 days). This is **low QPS, high correctness**.
- **Say it straight**: "It isn't a throughput problem; it's a **correctness** problem: money, a proprietary format, and no second chance."
- 美元量级不说（口径未对齐）。
- **Follow-up: peak?** 【待补：峰值倍数、单文件行数、批处理耗时】
- **Follow-up: bottleneck?** I have no published numbers; I'd measure **time per stage** and **rows per second**.

### A4 · 数据模型和键怎么设计？
- **Staging**: one line per row, **record type** cut from the first 10 characters.
- **Typed tables**: six record types, each its own table, fields cut by **offset** in procedures, with `TRY_TO_DECIMAL` / `TRY_TO_DATE` so a bad field becomes NULL, not an abort.
- **Composite key** = **reference number + reject indicator**: a settled and a rejected record **coexist**; the validator decides.
- **Follow-up: why not just the reference number?** A later **reject** would overwrite the **settled** record.
- **Follow-up: implied decimals?** Amounts carry **implied decimal places**, divided on parse; a validation catches a wrong scale. 【待补：校验方式】

### A5 · 怎么保证不重复、不丢？
- **Idempotent at three layers**: **file load history** (`COPY INTO` doesn't reload a file), **`MERGE` keys** at every stage, **error log** (rejects kept, never dropped).
- **Not exactly-once**: **at-least-once plus idempotent writes** is effectively once.
- **Streams are not transactional** with the writes: correctness comes from the **downstream `MERGE` key**, not the stream.
- **Follow-up: file re-delivered?** Load history skips it; if it is reprocessed, the `MERGE` is a **no-op**.
- **Follow-up: two upstream tasks out of step?** `AFTER A, B` guarantees each ran, **not on the same batch**; mismatches go to the error log and **self-heal** next run.

### A6 · 生产里坏过什么？
- **Late file**: a file landed in **yesterday's folder** after we'd moved on; I now scan **all date partitions** by pattern and rely on **load history** for dedup.
- **Reject after settle**: the composite key lets both states coexist.
- **Stream staleness**: **silent if unconsumed**. 【待补：实际怎么监控】
- **Noise**: the error log has entries that **disappear next run**; the runbook separates them.
- **Follow-up: impact of the late file?** The downstream had already produced one version with **less data**; the next run picked it up.
- **Follow-up: any incident on this line?** S3 sits **downstream**; I say "when it broke, the pipeline **recorded** it instead of dropping it".

### A7 · 你怎么知道它是对的？
- **Row**: `TRY_TO_DECIMAL`: a bad field doesn't kill the batch.
- **Batch**: health checks assert **every settled transaction has its fee**.
- **Reconciliation**: fee totals against the **summary record** Amex itself sends; a mismatch **halts** the task and **pages** on-call (me).
- **Follow-up: what does the check not cover?** It can't tell a wrong parse from a **consistent** wrong parse; the Amex summary is the independent anchor.
- **Follow-up: how fast do you find out?** 【待补：从告警到根因的真实时间】

### A8 · 瓶颈和性能
- **Honest first**: "I have **no published throughput numbers** for it."
- **How I'd find the bottleneck**: **time per stage**, **rows per second**, then **warehouse cost** per run; look at the **query profile** for the `MERGE`.
- **Already done**: **gating** so nothing runs on empty input; **separate streams** so consumers don't block each other.
- **Follow-up: where would you expect it?** The `MERGE` against a growing typed table: bounded by **key lookups**; I'd check **pruning** first. 【待补：是否看过】
- **Follow-up: warehouse cost?** The gate on stream data keeps cost **proportional to work**.

### A9 · 你接受了哪些取舍？
- **Weaker orchestration** than Airflow; mitigated with monitoring.
- **Six parsers** repeat one **offset table**: simple to read, expensive to extend.
- **Feature flag per region** (EU got a second): needs **manual consistency checks** between environments.
- **Late files** processed on the next run: the downstream may have **one stale version**.
- **Follow-up: which one hurt most?** 【待补：你的真实判断】

### A10 · 重来你会改什么？
- **Config table + one generic fixed-width parser**: a seventh record type becomes a **config row**, not a new procedure. I used that pattern later in the quality-check framework.
- **Make the unmapped case an explicit error** where categories are derived (the S3 lesson).
- **Follow-up: why didn't you do it the first time?** The first delivery needed to land; the duplication was visible only after **six** copies.

### A11 · 如果数据量大 100 倍，或者来源变成实时流？
- **Reasoning, not something I ran.**
- **100× files**: partition work by **day or file**, make the heavy step **incremental**, keep the idempotent keys; measure first.
- **Real-time source**: consume a **log** with partitioning and keep the **same idempotent writes**; the composite key and the error log carry over.
- **What I haven't done**: operate a streaming system at that scale.
- **Follow-up: what breaks first?** Probably **stream offsets** and the `MERGE` cost; I'd test with **replayed** production files.

### A12 · 发布和回滚
- **Kill switch**: a **feature flag** routes Amex into this separate flow without touching the path other networks use; **one `UPDATE`** turns it off, no release.
- **EU extension**: a **second flag** and a separate fee ledger.
- **Follow-up: how do you roll back data?** **Fix forward**: wrong state may be consumed downstream, so you need a **correcting entry**, not a reversal.
- **Follow-up: environment drift?** 【待补：怎么核对各环境的开关一致】

### A13 · 哪些是你做的，哪些不是
- **Mine**: the topology, staging and stream design, six parsers, validators, fee task, kill switch, EU extension, about a dozen hardening PRs, the design doc.
- **Not mine**: the Ruby payout service that used to hold this logic; the downstream payout.
- 不说 "top committer"、"parsing UDTFs"（解析在 procedure 的 SUBSTRING 里，校验才是 UDTF）。
- **Follow-up: who reviewed the design?** 【待补：评审的人和他们的意见】
- **Follow-up: data sensitivity / access control?** 【待补：文件里有什么敏感字段，谁能读】

## 项目 B · interchange 数据源切换（S5）

### B1 · 30 秒讲清楚这个项目
- **Context**: pass-through fees came from the acquirer's **transaction view**, which sometimes filled **after the payout cutoff**; a **settlement view** arrives earlier.
- **Mine**: I owned the **interchange-fee track**: move the biggest category, credit interchange, to the earlier source.
- **Result**: **13.7M rows** cut over at **>99.9%** field parity; **deploy and release** were separate steps.
- **Boundary**: "I own the **fee side**; the program owner of record is someone else."

### B2 · 为什么这样决策：两个方案怎么比
- **A**: make the "whichever view has data" **fallback** smarter. **B**: a **static split by fee type**.
- **Chose B**: the fallback already had **sticky state and three CTEs**; "a **source of truth** should be a **fact**, not a runtime decision."
- **Cost of B**: a **migration toggle** and a hard split I must keep consistent.
- **Follow-up: did anyone prefer A?** 【待补：有无资深同事倾向 A，怎么说服的】
- **Follow-up: what would change your mind?** If parity had been **below the bar** or differences **unexplained**.

### B3 · 怎么验证
- **Discovery**: both sides in the same shape, **full outer join** with `EQUAL_NULL`, field by field: **>99.9%**; the **0.07%** mismatches were all **one-sided same-day** records (timing, not conflict); two differences explained.
- **Pre-cutover**: the **production query itself** as `count(*)` on a full day: **13,737,670 vs 13,768,430**, **+0.224%**.
- **Two different numbers**: 0.07% is **field-level**; 0.224% is **row-count**; don't mix them.
- **Follow-up: why +0.224% is acceptable?** 【待补：当时怎么解释这个差】
- **Follow-up: why use the production query?** No gap between what I **tested** and what I **shipped**.

### B4 · 幂等和键
- **Idempotent `MERGE`** on a **synthetic key** = prefix + invoice number; the task re-runs **hourly**, a re-run is a **no-op**.
- **Idempotency lives in the data's uniqueness**, not in an external state machine.
- **Follow-up: duplicate invoice numbers?** 【待补：是否出现过；怎么处理】
- **Follow-up: why `EQUAL_NULL`?** It treats **NULL = NULL** as equal, so keys with NULLs still match.

### B5 · 为什么给 ON 加时间窗口，代价是什么
- **Why**: staging only grows, so an equality `ON` scans **all history**; a **one-month window** lets **zone maps prune** and keeps scan cost **constant**.
- **Cost**: a record reprocessed **after a month** bypasses dedup; I **documented** it beside the clause.
- **Follow-up: how do you know pruning worked?** Read the **query profile** (partitions scanned vs total). 【待补：是否真的看过；没有就说「I reasoned it from the clustering」】
- **Follow-up: faster by how much?** I did not measure it; never say "N× faster".

### B6 · 上游没准备好怎么办
- **Quality gate**: the merge joins the **trigger-status** table; until the upstream says the day is **validated**, the join returns **nothing**; fees **wait**, never read half-built.
- **Merchant-level gate** and **Amex excluded** (own pipeline).
- **Follow-up: settlement view late too?** Same: nothing is written, fees wait.
- **Follow-up: where does the status come from?** The quality-check framework ([[S2]]): all enabled checks pass → `Completed`.

### B7 · 怎么避免重复计费
- The old task **skips interchange** when the toggle is on; the new one writes it.
- **Source filtering**, not `MERGE` dedup, makes the two paths **exclusive**.
- **Follow-up: why not dual-write?** Two tasks gated in **opposite directions** by one toggle *are* the exclusion; dual-write without it **double-charges**.
- **Follow-up: what if the toggle flips mid-run?** 【待补：任务边界与开关读取时点】

### B8 · 发布、回滚和时间窗口
- **Ship dark**: merged with the toggle **off**; enabled in **pre-prod**, then production.
- **Cron window** derived from when the settlement view is **actually ready**.
- **Rollback**: flip the toggle: a **fast off**. 【待补：是否真的用过】
- **Follow-up: how long was the rollout?** 说「shipped dark, enabled in pre-prod, then production」；不说「merchant by merchant」、「两周」。
- **Follow-up: deploy vs release?** Deploy puts code in; **release** is turning the toggle on.

### B9 · 哪里还会出错
- **Reprocessing past the window**: the dedup blind spot.
- **One-sided same-day records**: they arrive later and are picked up then.
- **Two explained differences**: a sequence-code field and an alternate dispute id.
- **Follow-up: how would you detect a regression after cutover?** Keep the parity query as a **running check**, not a one-off. 【待补：是否做了】
- **Follow-up: worst case?** Fees wait for a day: **late, not wrong**.

### B10 · 规模数字
- **Mine**: **13.7M rows** cut over, **>99.9%** parity, **+0.224%** row-count difference.
- **Program-level, not mine**: the **$55B** incremental volume and the **~$450M a month** float the program frees.
- **Follow-up: how long is the program?** A multi-quarter program; I say "my track inside it".

### B11 · PostgreSQL 和 Snowflake 怎么分工
- **PostgreSQL**: OLTP, **system of record** for pricing schedules; **unique constraints**; atomic header + N fee rows.
- **Snowflake**: where we **aggregate** across very large tables.
- **Sync**: application-level **idempotent upsert**; conflicts surface as `FAILED_PRECONDITION`.
- **Follow-up: net settlement in Postgres?** One **flag** on the pricing schedule.
- **Follow-up: why not one database?** OLTP guarantees vs analytic scans: different workloads.

### B12 · 重来你会改什么
- **Put the parity query into monitoring** after cutover, not only before.
- **Record partitions scanned** before and after the window, to turn a reasoned claim into a measured one.
- **Make the toggle's read time explicit** in the task.
- **Follow-up: any regret?** 【待补：你的真实回答】

### B13 · 你学到了什么，之后怎么复用
- **Validate with the thing you ship; bound the scan; ship dark.**
- The **backfill SQL** became the team's **CDC backfill template**.
- **Follow-up: where did you apply it again?** 【待补：下一个用到同一套做法的项目】
- **Follow-up: how does it relate to growth work?** Experiments need the same discipline: **a number you can re-run**, and **the time it was read**.
