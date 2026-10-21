# S1 · 简历主线：结算管线"出错就记下来，绝不丢掉"（简历深挖 · 幂等 · 可观测）

用于：walk me through your resume / biggest system / how do you know it's correct / what broke in production。

**Hook：「I built a settlement pipeline whose rule is: when data is wrong, record it, never drop it.」**

## 数字

- 约 2,200 万笔 Amex 交易（半年）；18 个月生产；最大单个 PR 约 1,800 行；约 90 个 PR。
- 美元量级不说（口径未对齐）。

## 60 秒

**S**
- **Amex** is a closed-loop network: one **fixed-width file a day**. We can't book a transaction until the file **confirms** it settled.

**T**
- I inherited a **stub with one table** and owned the pipeline **end to end**, design doc to **18 months** of production.

**A**
1. A scheduled task runs `COPY INTO` from S3 into a **staging table**, one line per row.
2. **Six append-only streams**, one per **record type**, each with its **own offset**.
3. Six procedures cut the fields and `MERGE` on a **composite key**.
4. Two table functions **validate** with a full outer join; mismatches go to an **error log**, never dropped.
5. A downstream task with **two upstream dependencies** computes the fee in **one transaction**.
6. **Idempotent at three layers**: file load history, `MERGE` keys, error log. Behind a **feature flag** = a **kill switch**.

**R**
- ~**22M transactions** in half a year; **18 months** live.

**L**
- **At-least-once plus idempotent** beats chasing exactly-once; **bad data is recorded, not dropped**.

## 2 分钟（在 60 秒上加）

- **Why separate streams**: independent **offsets**, so consumers don't block each other. Streams aren't transactional with the writes, so correctness comes from the **downstream `MERGE` key**.
- **Composite key** = reference number + **reject indicator**: a settled and a rejected record **coexist**; the validator decides.
- **Gating**: `SYSTEM$STREAM_HAS_DATA` so a warehouse **never spins up on empty input**.
- **Three correctness layers**: **row** (`TRY_TO_DECIMAL`, a bad field doesn't kill the batch), **batch** (health checks), **reconciliation** against Amex's own summary record; a mismatch **halts** and **pages** on-call (me).
- **Failure: late files**: a file landed in **yesterday's folder**; I scan **all date partitions** by pattern and rely on **load history** for dedup.
- **Monitoring**: a task monitor and Datadog alerts driven by health-check procedures. **EU extension** with a second flag.
- **Different next time**: the six parsers repeat one offset table; use a **config table + one generic parser**.

## 追问

- **What exactly was yours?** Everything from the **topology** onward, ~a dozen hardening PRs; the **largest PR** is this pipeline.
- **Why not Airflow or Spark?** **Data locality** and **transactional** steps in the warehouse; cost is **weaker orchestration**, so I built monitoring on top.
- **No duplicate, no lost fee?** Every stage **idempotent**; rejects **kept**.
- **Exactly-once?** No; at-least-once plus idempotent writes is **effectively once**.
- **Two upstream tasks out of step?** `AFTER A, B` guarantees each ran, not on the **same batch**; mismatches go to the error log and **self-heal** next run.
- **Stream staleness?** Silent if unconsumed. 【待 Chi 补：实际怎么监控】
- **Bottleneck?** I'd measure **time per stage** and **rows/second**; I have no published numbers.

## 别说

- "top committer / 615 commits"；"no bugs"；"parsing UDTFs"（解析在 procedure 的 SUBSTRING 里）。
- "I migrated Funding's Ruby scripts"；美元数。

## 待 Chi 补

- 第二个按这套模式接入的来源；设计评审里的反对意见；任何真实吞吐/耗时。
