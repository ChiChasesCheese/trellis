---
title: Chakra scenarios · 12 道场景题
aliases:
  - Chakra scenarios
tags:
  - company/snowflake
  - round/ai-screen
---

# scenarios · Applied scenarios（后端应用场景，口述框架，English）

> 邀请邮件第二段 "Applied scenarios relevant to your role"。一手报告说 Chakra 轮无 coding，所以是**口头推理题**。打分要的是 "structured reasoning + specific examples"，每题用同一个骨架：
> **Clarify（1 句）→ Approach（3 步）→ What I actually did that's closest（1 个真实例子 + 量级）→ Trade-off / what I'd watch（1 句）**。每题 60–90 s。
> 12 题按「Snowflake backend JD 最可能问」排序，每题标出命中的 JD 线：**SQL · DS（distributed systems） · DBI（database internals） · Prod（large-scale production） · Java**。故事编号可点：[[S1]]…[[S11]]。

## 通用开场句（任何场景题都先说这句）

> "Let me structure this: first what I'd want to know, then how I'd approach it, then the closest thing I've actually done."

---

## 1. "A nightly pipeline that computes customer charges starts producing wrong totals for a subset of customers. How do you find and fix it?" — SQL · Prod

> **Clarify**: Is it wrong for a subset by customer attribute, or by time — did it start on a specific day? That tells me whether it's a data change or a code change.
>
> **Approach**: One — scope it with data before touching code: query the affected versus unaffected population and diff their attributes; the discriminating attribute usually names the bug. Two — walk backwards from the wrong output through each stage's intermediate table until the numbers diverge; that's the stage to read. Three — one hypothesis, verify it with a query, ship the minimal fix plus a backfill, and add the invariant check that would have caught it.
>
> **Closest thing I did**: A health check I'd built paged: some transactions had no fee. Scoping showed 100 percent were bank-account transactions on a new path — a couple of hundred merchants. Walking back, the fee-category key was `'BT_' || sub_kind`, sub-kind was `NULL` for that population, and `NULL` concatenation yields `NULL` in SQL, so no fee row was generated — silently. Root cause: a shared `MERGE` re-deriving the field with the wrong UDF overload. I wrote the postmortem including why four e2e tests missed it, then removed the two-overload design so it can't recur.
>
> **Trade-off**: Fix forward with a backfill rather than roll back — in billing the wrong state has already been consumed downstream; you need a correcting entry, not a reversal.

→ [[S3]]

## 2. "Design a service that meters usage events and produces a daily bill, so that retries never double-charge." — DS · SQL

> **Clarify**: Are events delivered at-least-once? I'll assume yes — that's the realistic case — and that a bill must be reproducible after the fact.
>
> **Approach**: One — every event carries an idempotency key (source, sequence or event id); ingestion is an upsert keyed on it, so a retry is a no-op. Two — aggregation is a deterministic function over the immutable event set for the day, materialized with `MERGE` keyed on (customer, day, meter), so re-running aggregation is also idempotent. Three — reconciliation as a separate job that recomputes from raw and compares against the bill; discrepancies block invoicing and page someone. Late events become a next-cycle adjustment line — never mutate a closed day.
>
> **Closest thing I did**: This is the shape of our fee pipeline. Files can arrive twice, tasks retry; `COPY INTO` dedups at the file level, every stage is a `MERGE` on natural keys, and fee totals reconcile against the summary record the network itself sends. When I switched our interchange source I ran the production query as a shadow `count(*)` before enabling the toggle.
>
> **Trade-off**: Idempotent upserts cost a unique key and make ingestion slightly slower; dedup at aggregation time is faster to ingest but makes the raw layer untrustworthy — and in billing the raw layer is your audit trail.

→ [[S1]] · [[S5]]

## 3. "You need to change the schema of a large production table — or switch its source of truth — without downtime." — DS · DBI

> **Clarify**: Are readers and writers under my control, and can I afford to run two paths in parallel for a while? I'll assume yes.
>
> **Approach**: Expand-migrate-contract. One — add the new column or source alongside the old; nullable columns only, so old and new code coexist during a rolling deploy. Two — shadow-read: compute from both and compare at scale, in production, before anyone depends on the new one. Three — flip readers behind a flag; rollback is the flag. Four — contract: remove the old path only after a full cycle without discrepancies.
>
> **Closest thing I did**: Switching credit interchange from the acquirer's transaction view to the settlement view. Discovery pass with a `FULL OUTER JOIN` and `EQUAL_NULL` field by field — over 99.9 percent parity, every difference explained; then the production query itself as `count(*)` over a day, about fourteen million rows, within a fraction of a percent. Shipped with the toggle off, enabled in pre-prod, then prod. The old task was modified to exclude interchange only when the toggle is on — so the two paths are complementary and can never double-count.
>
> **Trade-off**: Dual-running doubles compute for a few weeks — worth it when the table is revenue; for a low-stakes table I'd do a single backfill with a verification query.

→ [[S5]]

## 4. "A query or a service got slow after a deploy. Walk me through it." — DBI · Prod

> **Clarify**: Slow for everyone or for one tenant? Latency or throughput? Did data volume or a dependency change at the same time?
>
> **Approach**: One — confirm with metrics, not reports: p50 vs p99, before vs after the deploy timestamp. Two — bisect: what changed, and can I A/B old and new on the same input. Three — for a query, read the profile: partitions scanned versus total — did pruning stop working, did a join fan out, did a function start running per row instead of set-based. Four — revert first if customers are affected, then reproduce offline.
>
> **Closest thing I did**: Two shapes. In a `MERGE` into an ever-growing staging table, the `ON` clause had only an equality — every run compared against all of history. I added a time window on the target's `created_at` so the zone maps prune to the last month; scan cost went from growing with the table to constant. And in an anomaly-detector handoff, per-row numpy scoring that was fine on QA would have timed out on a 760-million-row production day; the fix was pushing the deterministic rule down to set-based SQL.
>
> **Trade-off**: The window trades a tiny chance of missing a very late duplicate for bounded cost — so the invariant is documented next to the clause.

→ [[S5]] · [[S6]]

## 5. "You're on call and a partner reports their payouts are delayed. What do you do in the first 30 minutes?" — Prod

> **Approach**: One — blast radius and clock: which partner, how many accounts, since when, and what the SLA actually is. Two — stuck versus late: is our pipeline behind, or did the upstream not settle to us yet. Three — an interim update within fifteen minutes with what we know and when the next update is. Four — one owner per hypothesis, not everyone chasing the same one.
>
> **Closest thing I did**: A large marketplace merchant reported millions in Amex payouts missing. The incident commander named me one of three fix owners. The SLA question came to me: T+7 is our internal pipeline SLA and we only disburse after the network settles to us — that separated expected latency from the real regression, which was an effective-date change made for EU compliance shifting US dates by a day. I argued for a region conditional in the table function rather than a revert, so EU and US keep independent semantics.
>
> **Trade-off**: The temptation is to start fixing; the first ten minutes are better spent on scoping and a clear statement of what's actually broken.

→ [[S9]] · [[S8]]

## 6. "How would you build a rate limiter / quota system shared by multiple upstream services?" — DS

> **Clarify**: Per-tenant or global? Exactness, or is ~1 percent overshoot acceptable? Cost of a false reject versus a false accept?
>
> **Approach**: One — token bucket per (tenant, resource): refill rate and burst are two knobs everyone understands. Two — shared store with an atomic decrement — Redis with a Lua script, or a database row with a conditional update. Three — avoid the hot key: shard the bucket and give each service a small local allowance so the common path doesn't hit the store. Four — return remaining quota in the response so clients back off before rejection; emit rejects-per-tenant as a metric.
>
> **Closest thing I did**: Not a rate limiter in production, but the same concurrency shape: a lease-based account scheduler with `locked_until`, and Snowflake's own controls — `SUSPEND_TASK_AFTER_NUM_FAILURES`, auto-retry attempts, and the "stream has data" gate so tasks don't consume warehouse credits on empty input. I've also drilled the four-part rate-limiter design — global, per client, weighted fairness, idle cleanup — as prep.
>
> **Trade-off**: Exactness costs a round trip per request; a local allowance trades bounded overshoot for latency. For billing quotas, exact; for API smoothing, approximate.

## 7. "Events arrive from Kafka into a warehouse. How do you get exactly-once results?" — DS · SQL

> **Clarify**: Exactly-once delivery or exactly-once *effect*? Delivery is at-least-once in practice; I design for exactly-once effect.
>
> **Approach**: One — the consumer commits offsets after the write, not before; at-least-once at the transport. Two — the write is idempotent on a business key — `MERGE ... WHEN NOT MATCHED` — so duplicates are no-ops; keep the idempotency decision inside the database's atomic statement, not in "check then insert" application code, which has a TOCTOU race. Three — replay is a first-class tool: because writes are idempotent, re-consuming from an offset is safe, which is how you fix a bug in the transformation logic.
>
> **Closest thing I did**: Our gateway publishes transaction events to Kafka; Snowpipe Streaming lands them in a raw table; a Stream and Task move them through a table function into typed pending and transactions tables with `MERGE` on the public id. As an intern I built the Kafka-to-Snowflake connector path with a protobuf converter and poison-message isolation. The lesson I carry: an append-only stream's offset advance and your business write are not one transaction — so correctness lives in the downstream key, never in the stream.
>
> **Trade-off**: Auto-commit with a short interval is simpler but leans at-most-once under crashes; I'd rather commit-after-write and pay for idempotency.

→ [[S1]] · [[TS02]]

## 8. "Downstream teams keep reading a table before it's complete. Design a mechanism so they never read bad or partial data." — DS · SQL

> **Clarify**: Are consumers in the same database — or across databases and accounts? I'll assume across, which rules out task dependencies.
>
> **Approach**: One — separate "written" from "ready": a per-(subject area, date) status row that flips to `Completed` only when every enabled quality check passes. Two — make readiness a `JOIN` condition in the consumer's query, not a Slack message: if the row isn't `Completed`, the query returns nothing. Three — checks are config, not code: a contract table names the procedure, the date column, the SLA; a generic executor runs them and writes normalized results. Four — an SLA monitor pages when a subject area isn't `Completed` by the cutoff.
>
> **Closest thing I did**: That's the quality-check and trigger-status framework I built and rolled across eight subject areas; the status table is replicated to a share layer and my interchange procedure joins on `STATUS = 'Completed'`. The follow-on ADR I drove takes readiness to merchant level, so fifty bad merchants stop blocking thirty-five thousand — with a "strictest wins" rule so mixed deployments stay safe.
>
> **Trade-off**: Handshake solves timing, not content — if a check doesn't cover a class of error, the flag is green and the data is wrong. That's why the checks are the real product.

→ [[S2]]

## 9. "Two systems disagree on a number — say the fees you computed versus what the acquirer reports. How do you find out who's right and fix it?" — SQL · Prod

> **Clarify**: Do both sides have a shared key at the record level, or only aggregates? And which side is the legal source of record?
>
> **Approach**: One — normalize both sides into the same shape and `FULL OUTER JOIN` on the business key with `EQUAL_NULL`, so one-sided records are classified, not lost. Two — bucket the differences: present on one side only, present on both with field mismatch, and timing — then explain every bucket before touching anything. Three — fix the pipeline for the systematic bucket, backfill the historical one, and turn the join into a daily reconciliation check.
>
> **Closest thing I did**: The discovery pass before switching interchange sources — field-by-field parity over ninety-nine-point-nine percent, and the residual was records present only on one side for the day, not true conflicts. And a refund-fee postmortem where my own first blast-radius predicate was wrong; adding "the new pricing schedule existed at fee-creation time" took the scope from two hundred thousand rows to twenty-two thousand. I'd rather retract my own number than let a remediation be sized off a bad predicate.
>
> **Trade-off**: A reconciliation that only compares totals hides offsetting errors; record-level costs more compute and is the only one I'd trust for money.

→ [[S5]] · [[S10]]

## 10. "Design a scheduler for dependent batch jobs with retries and backfills." — DS · DBI

> **Clarify**: Are jobs idempotent? If not, retries are dangerous and that's the first thing to fix.
>
> **Approach**: One — a DAG where each node declares its predecessors; a node with two upstreams runs only after both complete. Two — trigger on data, not on the clock: "run when the upstream has new rows" avoids empty runs and lets late data flow naturally. Three — retries with a failure budget: auto-retry N times, then suspend and page; a suspended node must be resumable without replaying its predecessors. Four — backfill is just "re-enqueue rows into the input," which only works if every node is idempotent.
>
> **Closest thing I did**: That's how our fee DAG is built on Snowflake Tasks: `AFTER A, B` for the fee-calculation node, `WHEN SYSTEM$STREAM_HAS_DATA` as the data trigger, `SUSPEND_TASK_AFTER_NUM_FAILURES` and auto-retry, and cron windows reverse-engineered from when the upstream actually flips to complete. The subtle failure I've handled: `AFTER A, B` guarantees both ran, not that they processed the same batch — so the join in the fee validator is a `FULL OUTER JOIN` that records a miss and self-heals on the next run.
>
> **Trade-off**: Data-triggered DAGs are cheap and simple but have weaker orchestration than Airflow — no branching, no external callbacks — so you invest in observability instead.

→ [[S1]]

## 11. "A table has billions of rows and queries against it keep getting slower. What do you do?" — DBI · SQL

> **Clarify**: What do the slow queries filter on — dates, tenants, both? And is it scan time or skew?
>
> **Approach**: One — read the query profile: partitions scanned over partitions total. If most partitions are read, pruning is broken. Two — align physical layout with the dominant predicate: a clustering key on the high-frequency filter column, moderate cardinality, prefix first; accept that one layout serves one access pattern and build a summary table for the other. Three — if a few workers take all the time, it's skew — `NULL`s, one giant tenant, a default value — and adding compute won't help; fix the key or isolate the tenant. Four — bound the scan in the query itself: a time window on the join or merge predicate so zone maps can prune.
>
> **Closest thing I did**: Our fee and transaction tables carry explicit `CLUSTER BY` on the settlement-date and merchant-reference columns that every query filters on; and the time-windowed `MERGE` I described turned a scan that grew with history into a constant one. In the merchant-level quality-check design I rejected a `VARIANT`-plus-UDF option specifically because a secure view over a per-row UDF disables predicate pushdown on a table that size.
>
> **Trade-off**: Clustering costs background compute forever; if the key isn't in the common filter, you pay maintenance for nothing.

→ [[TS09]]

## 12. "Data arrives late or out of order in a daily batch. How do you keep the day's results correct?" — DS · SQL

> **Clarify**: Can a closed day be reopened, or must corrections be adjustments? In finance, closed days are closed.
>
> **Approach**: One — separate arrival time from effective time; store both. Two — ingestion must accept late data without special-casing: scan all partitions, dedup by content, let the late rows flow through the same idempotent path. Three — the closed-day rule: a late record becomes an adjustment on the day it arrives, with a pointer to the day it belongs to; never mutate the closed aggregate. Four — a health check on "expected but not yet arrived" so lateness is visible before someone downstream notices.
>
> **Closest thing I did**: Amex dropping a file into yesterday's date folder after we'd moved to today. I changed ingestion to a `PATTERN` regex over every date partition and leaned on `COPY INTO`'s load history for dedup; late files are picked up next run. And an effective-date change for one region shifted another region's disbursement dates by a day — the fix was region-conditional effective-date logic in the table function, not a revert.
>
> **Trade-off**: Accepting late data everywhere means the day's first answer can be incomplete — so every consumer has to be built to see a version, not "the" number.

→ [[S1]] · [[S9]]

---

## 如果它出了不在上面的题

先说通用开场句，然后 Clarify → 3 步 → 最接近的真实例子 → trade-off。**没做过就说没做过**："I haven't built X, but the closest thing I've done is Y — and here's how I'd approach X." 真实例子池：[[S1]]–[[S10]]，加 Stripe 题库里做过的 q07 订阅调度、q13 ledger、q25 对账、q18 union-find 风控。技术栈讲法与边界：[[Tech Stacks]]。
