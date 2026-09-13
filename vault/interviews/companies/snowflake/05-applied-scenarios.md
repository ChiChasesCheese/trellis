# 05 · Applied scenarios（后端应用场景，口述框架，English）

> 邮件第二段 "Applied scenarios relevant to your role"。一手报告说 Chakra 轮无 coding，所以是**口头推理题**。打分要的是 "structured reasoning + specific examples"，所以每题用同一个骨架：
> **Clarify（1 句）→ Approach（3 步）→ What I actually did that's closest（1 个真实例子 + 数字）→ Trade-off / what I'd watch（1 句）**。每题 60–90 s。
> 六题按「Snowflake backend 最可能问」排序；每题末尾注明对应的故事。

## 通用开场句（任何场景题都先说这句）

> "Let me structure this: first what I'd want to know, then how I'd approach it, then the closest thing I've actually done."

---

## 1. "A nightly pipeline that computes customer charges starts producing wrong totals for a subset of customers. How do you find and fix it?"

> **Clarify**: Is it wrong for a subset by customer attribute, or by time — did it start on a specific day? That tells me whether it's a data change or a code change.
>
> **Approach**: One — scope it with data before touching code: query the affected vs unaffected population and diff their attributes; the differentiating attribute usually names the bug. Two — walk backwards from the wrong output through each stage's intermediate table until the numbers diverge; that's the stage to read. Three — form one hypothesis, verify it with a query, ship the minimal fix plus a backfill, and then add a quality check that would have caught it.
>
> **Closest thing I did**: A PagerDuty fired that some transactions had no Braintree fee. Scoping showed 100% of the affected rows were standard ACH — about 196 merchants, 11 million dollars a day. Walking back, the fee-category key was `'BT_' || sub_kind`, and sub_kind was NULL for that population, and NULL concatenation yields NULL in SQL, so no fee row was generated. Root cause was a new two-argument UDF overload while the promotion path still called the one-argument version. Fixed the call, backfilled, consolidated the overloads so it can't recur, and added a non-null assertion on category keys to our quality-check framework.
>
> **Trade-off**: I fix forward with a backfill rather than roll back, because in billing the wrong state has already been consumed downstream — you need a correcting entry, not a reversal.

→ S3 · `core/answers` Q3

## 2. "Design a service that meters usage events and produces a daily bill, so that retries never double-charge."

> **Clarify**: Are events delivered at-least-once? I'll assume yes — that's the realistic case — and that a bill must be reproducible after the fact.
>
> **Approach**: One — every event carries an idempotency key (source, sequence or event id); ingestion is an upsert keyed on it, so a retry is a no-op. Two — aggregation is a deterministic function over the immutable event set for the day, materialized with MERGE keyed on (customer, day, meter), so re-running aggregation is also idempotent. Three — reconciliation: a separate job recomputes totals from raw and compares against the bill; discrepancies block invoicing and page someone. Late events go into the next cycle as an adjustment line, never by mutating a closed day.
>
> **Closest thing I did**: This is literally the Amex fee pipeline. Files can arrive twice, tasks retry; every stage is a MERGE on natural keys, and the fee totals are reconciled against the summary record Amex sends. In 2025 that handled about 22 million transactions and 138 billion dollars without a double-count. For the net-settlement cutover I ran a shadow reconciliation — 13.7 million rows, 0.224% variance, every category explained — before switching sources.
>
> **Trade-off**: Idempotent upserts cost you a unique index and make ingestion slightly slower; the alternative — dedup at aggregation time — is faster to ingest but makes the raw layer untrustworthy, and in billing the raw layer is your audit trail.

→ S1 · S5 · S2

## 3. "You need to change the schema of a large production table — or switch its source of truth — without downtime. How?"

> **Clarify**: Are readers and writers under my control, and can I afford to run two versions in parallel for a while? I'll assume yes.
>
> **Approach**: Expand-migrate-contract. One — add the new column or new source alongside the old; writers dual-write or the new source is populated by backfill. Two — shadow-read: compute results from both and compare at scale, in production, before anyone depends on the new one. Three — flip readers behind a flag, cohort by cohort, with a rollback that's just the flag. Four — contract: remove the old path only after a full cycle without discrepancies.
>
> **Closest thing I did**: Switching our interchange source from the transaction view to the settle view. I wrote a day-level shadow reconciliation over 13.7 million rows — over 99.9% field agreement — then rolled out merchant by merchant behind `US_CREDIT_INTERCHANGE_FROM_SETTLE_ENABLED`. That SQL became a reusable CDC backfill template on the team with a three-level fallback for timestamps.
>
> **Trade-off**: Dual-running doubles compute for a few weeks. Worth it when the table is revenue; for a low-stakes table I'd do a single backfill with a verification query and skip the shadow period.

→ S5

## 4. "A query or a service got slow after a deploy. Walk me through it."

> **Clarify**: Slow for everyone or for one tenant? Latency or throughput? Did anything else change — data volume, a dependency?
>
> **Approach**: One — confirm with metrics, not reports: p50 vs p99, before vs after the deploy timestamp. Two — bisect: what changed in the deploy, and can I A/B the old and new path on the same input? Three — for a query, read the plan: partition pruning lost, a join that became a cross join, a function that now runs per row instead of vectorized. Four — fix the regression first, optimize second.
>
> **Closest thing I did**: In our rules engine a change re-tokenized a rule string for every transaction row — the profile showed 3.98 seconds where we expected a fraction of a second. Hoisting the parse out of the row loop brought it to 0.28 seconds. Same shape in a Snowflake task: a UDF that was invoked per row where a set-based join did the same work.
>
> **Trade-off**: The fastest fix is often to revert; I revert first when customers are affected, then reproduce offline. Debugging live in production is only justified when a revert is impossible.

→ `core/stories/resume-evidence-map/03`（可观测性）· Stripe q12 的 perf 案例

## 5. "You're on call and a partner reports their payouts are delayed. What do you do in the first 30 minutes?"

> **Approach**: One — establish blast radius and clock: which partner, how many accounts, since when, and what the SLA actually is. Two — check whether the money is stuck or just late: is our pipeline behind, or did the upstream not settle to us yet. Three — communicate an interim update within 15 minutes with what we know and when the next update is, even if the answer is "still investigating." Four — assign owners for each hypothesis rather than everyone chasing the same one.
>
> **Closest thing I did**: The DoorDash Amex disbursement incident. The incident commander named me one of three fix owners. The key contribution was the SLA question: I established that T+7 is our internal US pipeline SLA and that we don't disburse until Amex settles funds to us — so the delay was upstream timing, not a pipeline failure — and the other owners deferred to that. That reframed the whole incident.
>
> **Trade-off**: Under pressure the temptation is to start fixing. The first 10 minutes are better spent on scoping and a clear statement of what's actually broken.

→ S9 · S8

## 6. "How would you build a rate limiter / quota system shared by multiple upstream services?"

> **Clarify**: Per-tenant quota or global? Do we need exactness or is ~1% overshoot acceptable? What's the cost of a false reject vs a false accept?
>
> **Approach**: One — token bucket per (tenant, resource) is the default: refill rate and burst capacity are two knobs everyone understands. Two — for multiple upstream services, the bucket has to live in a shared store; each service does an atomic decrement — Redis `DECR` with a Lua script, or a database row with a conditional update. Three — to avoid a hot key per tenant, shard the bucket and allow a small local allowance per service so the common path doesn't hit the store. Four — expose the remaining quota in the response so clients can back off before rejection, and emit metrics on rejects per tenant.
>
> **Closest thing I did**: Not a rate limiter in production, but the same concurrency shape: an account-scheduler with `locked_until` — acquire an account for a duration, LRU auto-select when none is specified — and Snowflake's own consumption controls, where I set resource monitors and task-level suspension after N failures. I've also drilled the four-part rate-limiter design — global, per client, weighted fairness, idle cleanup — as interview prep.
>
> **Trade-off**: Exactness costs a round trip per request; a local allowance with periodic sync trades a bounded overshoot for latency. I'd pick by the cost of a false accept — for billing quotas, exact; for API smoothing, approximate.

→ Stripe q23 / cd04 · q26

---

## 如果它出了不在上面的题

先说通用开场句，然后按 Clarify → 3 步 → 最接近的真实例子 → trade-off。**没做过就说没做过**："I haven't built X, but the closest thing I've done is Y — and here's how I'd approach X." 真实例子池：S1–S9 + Stripe 题库里做过的 q07 订阅调度、q13 ledger、q25 对账、q18 union-find 风控。
