# stories · Chakra 用的十个故事（English 口述稿，senior 口径）

> 每个故事一个固定骨架：**Headline（我拥有什么）→ Mechanism（怎么做的，说出工具名/原语名）→ Decision & trade-off（我选了什么、放弃了什么）→ Impact（量级词，不纠结精确数）→ What I'd change**。首答 60–90 s，追问版每条 ≤ 45 s。
> JD 加权关键词（Chakra 对 must-have 加权）：**SQL · distributed systems · Java · database internals · large-scale production · correctness · observability**。每个故事至少命中三个，粗体标出。
> 数字只保留量级（"tens of millions"、"billions of dollars"、"hundreds of millions of rows a day"），被追问精确值时说 "roughly" 即可；`04-answer-bank.md` §6 有一张数字卡。
> 故事本体的中文底稿在 `../../../../../core/stories/evidence-base.md`；技术栈讲法在 `../../../../../core/tech_stacks/`（01 系统设计 · 03 Snowflake · 07 CDC · 08 可观测性 · 09 SQL · 10 正确性）。

## 一图：题 → 故事

| 它问的方向 | 主故事 | 备用 |
|---|---|---|
| 最有代表性的项目 / 端到端 ownership | **S1** Amex 结算管线 | S5 |
| 平台化 / 定标准 / 被别人复用 | **S2** Quality-check 框架 | S7 |
| 最难的 bug / 生产事故 / on-call | **S3** ACH NULL 传播 | S8 · S9 |
| 跨团队 / 冲突 / 用数据说服 | **S4** AU Amex refund | S9 |
| 技术决策 + trade-off / 迁移 / 零停机切换 | **S5** Interchange 数据源切换 | S2 |
| 说不 / 推迟 / 判断力 | **S6** Anomaly detector go/no-go | S2 |
| 主动性 / 开发者效率 / AI 工具 | **S7** snowglobe-tools schema pool | — |
| 压力下快速 debug / unblock 团队 | **S8** Terraform 7 分钟 RCA | S3 |
| 事故指挥 / 领域权威 / SLA | **S9** Amex 出款延迟事故 | S4 |
| 推翻自己的结论 / 定量推理 | **S10** 退款费 billing-terms 复盘 | S3 |

---

## S1 · Amex 结算管线（旗舰：端到端 ownership + **SQL** + **database internals** + **large-scale production**）

**首答（90 s）**

> The project I'd pick is the American Express settlement pipeline on our Snowflake-native fee platform. Amex is a closed-loop network: instead of the near-real-time settlement views we get from our acquirer for Visa and Mastercard, Amex sends one proprietary **fixed-width reconciliation file** a day. That means we can't optimistically book an Amex transaction — it has to sit in a pending table until the file confirms it settled, which is our **good-funds model**.
>
> I owned the pipeline end to end, from the design document to eighteen months of production hardening. Mechanically: a scheduled Snowflake **Task** runs `COPY INTO` from S3 into a staging table, one line per row; six **append-only Streams** fan those rows out by record type; six stored procedures parse the fixed-width fields with offset-based `SUBSTRING` and `MERGE` them into typed tables on a composite key; two table functions validate the parsed records against the pending transactions with a `FULL OUTER JOIN` so that every mismatch lands in an error log instead of being dropped; and a downstream Task with **two upstream dependencies** computes the interchange fee per transaction inside one explicit transaction, then hands aggregates to our payout service.
>
> The design decisions I'd highlight: append-only streams so each record type has an independent offset and consumers don't block each other; `COPY INTO`'s file-level dedup plus composite-key `MERGE` at every stage, so retries and re-ingested files are idempotent; and a single feature flag that routes Amex into this separate flow without touching the code path every other card network uses. Later I extended it to the EU aggregator flow with a second flag and a different fee ledger.
>
> It's been processing tens of millions of transactions a year — billions of dollars — and it's the reference implementation the team points to for "how do we onboard a new file-based settlement source."

**追问版**

- **What was specifically yours?** → "I inherited a stub with one table. Everything from the topology onward is mine — the staging and stream design, the six parsers, the validation table functions, the fee-calculation task, the kill switch, the EU extension, and about a dozen hardening PRs. The largest single PR in my tenure — around 1,800 lines — is this pipeline. I also wrote the design doc the team reviewed."
- **Why Streams and Tasks instead of Airflow or Spark?** → "Data locality and transactional semantics. The file lands in Snowflake anyway; keeping parse-validate-compute inside the warehouse means every step is a `MERGE` inside a transaction and nothing leaves the account. `SYSTEM$STREAM_HAS_DATA` gates each task so we never spin up a warehouse on empty input. The trade-off is orchestration is weaker than Airflow — no branching, no external callbacks — so I built the observability on top: a Streamlit task monitor and Datadog alerts driven by health-check procedures."
- **How do you know it's correct?** → "Three layers. Row level: `TRY_TO_DECIMAL` and `TRY_TO_DATE` so a bad field never aborts the batch, and rejected records are kept, not dropped. Batch level: health checks assert every settled transaction has its fee, keyed on the pending table. Reconciliation level: fee totals reconcile against the summary record type Amex itself sends. A mismatch halts the task and pages the on-call — which has been me."
- **What broke?** → "Two things worth telling. First, file timing: Amex would drop a file into yesterday's date folder after we'd moved on to today. I changed the ingestion to scan every date partition with a `PATTERN` regex and rely on `COPY INTO`'s load history for dedup — late files are picked up on the next run instead of being lost. Second, the reject flag: a transaction can appear once as settled and later as rejected; I made the `MERGE` key composite — reference number plus reject indicator — so both states coexist and the validator decides which one wins."
- **What would you change?** → "The six parsers repeat the same offset table six times. I'd move field offsets into a config table and write one generic fixed-width parsing UDTF — adding a seventh record type becomes a config row, not a new procedure. That's exactly the pattern I used later in the quality-check framework."
- **How does this relate to what Snowflake builds?** → "I've been a very heavy consumer of Streams, Tasks, `MERGE` semantics, task DAG dependencies and warehouse cost controls for two years. I know where they're great and where they hurt — stream staleness is silent, task-level observability is thin — and that's the platform side I want to work on."

---

## S2 · 配置驱动的 Quality-check 框架（平台化 + **SQL** + **distributed systems** 的 handshake）

**首答（90 s）**

> The team had dozens of reconciliation tables — acquirer settlement, adjustments, tax, transaction reconciliation — and every new one got its own hand-written validation task. I replaced that with a **config-driven quality-check framework** that the whole team now onboards onto.
>
> Three pieces. A contract-config table: one row per (subject area, validation) that names the stored procedure to run, the date column, an SLA in hours and a JSON parameter blob. A generic executor that reads the config, builds the call with `EXECUTE IMMEDIATE`, captures the result through `RESULT_SCAN`, and writes a normalized PASS / FAIL / WARNING row — with an exception handler so one broken check never takes down the others. And a **trigger-status state machine**: when every enabled check for a subject area passes, the status flips to `Completed`, and that row is replicated to a share layer where downstream consumers `JOIN` on it. So "is this data safe to read" stopped being a Slack convention and became a `JOIN` condition in the consumer's SQL.
>
> Adding a check went from "write a new task, get it reviewed, deploy" to "insert a config row." I rolled it across about eight subject areas myself, and it's the mechanism my later interchange-source migration used to know the upstream settlement view was ready.
>
> The follow-on I'm proudest of is a design I drove after seeing a flaw in my own first version: readiness was per table, so roughly fifty bad merchants out of thirty-five thousand could block everyone. I wrote a formal ADR — four alternatives, a correctness argument that the table-level block always wins over merchant-level, and a volume analysis showing failures are the rare case so a sparse "one row per failing merchant" model costs almost nothing. That's the direction the team is taking the framework.

**追问版**

- **Why dynamic SQL — isn't that risky?** → "It's the price of config-driven. The config is engineer-controlled through migrations, not user input, so injection isn't the threat model; the real cost is losing static checking — a typo in a config row fails at runtime. I mitigated that with the exception handler and a health check on the results table itself."
- **Why a status table instead of task dependencies?** → "The consumers are in different databases, sometimes different accounts. A replicated status row is the lowest-common-denominator contract that crosses those boundaries; task `AFTER` dependencies don't."
- **Correctness argument in the ADR?** → "Strictest wins. The read query checks `NOT EXISTS (table-level failure)` before `NOT EXISTS (merchant-level failure)`, so a mixed deployment — some procedures refactored, some not — is always safe: an unrefactored procedure degrades to blocking everyone, which is today's behavior."
- **Why not VARIANT columns for the merchant list?** → "Two reasons from Snowflake internals: a secure view over a per-row UDF or VARIANT parse disables predicate pushdown, and I wasn't going to run that over a table with tens of millions of rows; and VARIANT has a per-cell size ceiling that a large merchant list can hit. Flat relational rows with an equality join keep pruning intact."
- **Status?** → "The framework and the eight rollouts are in production. The merchant-level extension is designed and reviewed; the core pattern is already proven in production for one subject area that writes per-merchant rows daily, and the framework-wide rollout is sequenced behind the net-settlement ramp." （不说"已上线"，但也不说"没批"——这是可以顶住追问的措辞。）

---

## S3 · ACH 费用 NULL 传播事故（最难的 bug + on-call + **SQL** 语义 + **correctness**）

**首答（90 s）**

> A daily health check I'd built — "every settled transaction has its Braintree fee" — paged the on-call. I forwarded the page to myself and had the root cause in the thread within a few minutes.
>
> The scoping query showed 100 percent of the missing fees were bank-account transactions on the new standard-ACH path — roughly two hundred merchants, on the order of ten million dollars a day of volume. Walking back through the stages: the fee calculation derives the pricing category as `'BT_' || payment_instrument_sub_kind`. For this population sub-kind was `NULL`, and in SQL `NULL` concatenation yields `NULL`, so the category matched nothing and no fee row was produced — silently. Why was it `NULL`? The pending-transactions procedure had two overloads of the same UDF; the shared final `MERGE` re-derived the field with the one-argument overload, which had no bank-account branch, overwriting the correct value the branch-specific logic had already computed.
>
> I wrote the postmortem: the evidence tables — a control group with the field populated had fees, a time series showing zero percent coverage at every age so it wasn't a lag — and the four specific reasons our end-to-end tests missed it, including a fixture that used a card payload for an ACH event. Then I owned the hardening: a stopgap first, then I removed the two-overload design entirely — one function with a defaulted second parameter, a versioned migration to drop the legacy signature so no future branch can pick the incomplete one — plus the e2e test that spans promotion to fee generation.

**追问版**

- **What did you decide, versus the team?** → "I made the call that the check was right and must not be suppressed — the fees were genuinely missing. There was pressure to add ACH to the exclusion list. I put the numbers in writing and the check stayed."
- **How did you avoid the same class of bug?** → "The principle I pushed: an unmappable payment instrument must fail loudly, not emit nothing. Silent `NULL` propagation is a SQL-language property, so the fix is a rule at the seam, not a patch at the call site."
- **Backfill?** → "Fix forward with a backfill rather than roll back — in billing the wrong state has already been consumed downstream, so you need a correcting entry, not a reversal."

---

## S4 · AU Amex 退款费（跨团队 + 用数据结束争论）

**首答（60 s）**

> A product manager escalated through our formal help process: Australian merchants weren't seeing Amex refund fees. It bounced across three teams in a fifty-reply thread before it was routed to me as the person who knows that domain.
>
> I pulled the data instead of the org chart: over a million refund-fee rows in the US over six months, zero in Australia, across about a hundred and fifty merchants. The root cause was configuration, not code — every AU merchant's pricing schedule had `fee_refund_policy = partial`, and the refund-fee logic only fires on `full`. I also showed it predated our platform migration, so it wasn't a regression we'd introduced.
>
> I wrote it up with the exact query so the PM and the other team could re-run it themselves. It ended the thread the same day and became a tracked feature to build the refund-fee pipeline properly. Giving everyone the same evidence beat arguing about ownership.

**追问**：*"A second, unrelated fee kind surfaced in the same thread — I said I wasn't certain, laid out a layered hypothesis, and a senior engineer confirmed it. I'd rather say 'not sure yet' with a plan than guess."*

---

## S5 · Interchange 数据源切换（技术决策 + **distributed systems** 迁移 + **SQL** 四层手法）

**首答（90 s）**

> Our pass-through fees — interchange, scheme, chargeback — all came from the acquirer's transaction-level view, and that view sometimes wasn't populated until after the daily disbursement cutoff, so fees missed the net-settlement window. I owned switching the biggest category, credit interchange, to the settlement view, which arrives earlier.
>
> Option A was to make the existing "whichever view has data" fallback logic smarter. Option B was a static split by fee type — interchange from settlement, everything else stays — behind a feature toggle. I chose B: the fallback had already grown sticky state and three CTEs, and in a revenue path I want the source of truth to be a fact, not a runtime decision.
>
> Before switching I did a discovery pass — a `FULL OUTER JOIN` with `EQUAL_NULL` field by field, over ninety-nine-point-nine percent parity, and every difference explained — then a pre-cutover run of the **production query itself as `count(*)`** over a day's data, about fourteen million rows, within a fraction of a percent. Validation and production share the same SQL, so there's no "validated one thing, shipped another."
>
> The procedure stacks four techniques: an idempotent `MERGE` on a synthetic key built from the invoice number; a **time-windowed `ON` clause** so the merge only scans the last month of an ever-growing staging table — that keeps the zone-map pruning intact; a `JOIN` on the trigger-status table so we never read a settlement day that hasn't passed quality checks; and a merchant-level feature gate plus an Amex exclusion, because Amex has its own pipeline. The old task was modified to exclude interchange only when the toggle is on, so the two paths are complementary and can never double-count. Shipped dark: merged with the toggle off, enabled in pre-prod, then production — deploy and release are two separate steps.

**追问版**

- **Trade-off of the time window?** → "If the same record is reprocessed more than a month later it bypasses dedup — a deliberate, documented risk in exchange for bounded scan cost. The invariant is written next to the clause."
- **Why not dual-write?** → "The two tasks are gated by one toggle in opposite directions — that *is* the mutual exclusion. Dual-write without an explicit exclusion condition is how you double-charge."
- **Reusable?** → "The backfill SQL became the team's CDC table-backfilling template."

---

## S6 · Anomaly detector 的 go/no-go（判断力 + 说不 + **large-scale**）

**首答（60 s）**

> I inherited an ML fee-anomaly detector from a departing intern. The easy path was to keep building. Instead I wrote a go/no-go assessment. QA had six synthetic merchants and under a billion rows; production is eighteen thousand merchants, fifteen thousand plan combinations, and up to seven hundred and sixty million rows on a peak day. The serving design was a per-row numpy forward pass — that would time out on a large warehouse, and QA could never have surfaced it.
>
> So I split it: what dies when the intern leaves versus what's reproducible from code — only the analyst labels were irreplaceable, and I got those persisted before their last day. Then a phased plan: Phase 1 ships only the deterministic consistency rule as pure SQL pushdown — `|amount| = rate × qty + fixed` — which Snowflake handles at billions of rows natively; Phase 2, the autoencoder retrain and serving redesign, is two to three months and gated behind an explicit business-driver decision. I froze the Slack alerting and CI/CD work until that gate says go. Results matter; I'd rather stop a project than ship one that pages the team at 3 a.m.

---

## S7 · snowglobe-tools：schema pool（主动性 + 开发者效率 + AI fluency + **database internals**）

**首答（60 s）**

> Nobody asked for this one. Our integration tests run migrations against a shared Snowflake schema, so two engineers — or two AI coding-agent sessions — on different branches collide on DDL. I built a **schema pool**: a `MAIN` schema synced to whatever commit is actually deployed to production — I query the GitHub Deployments API, not the release tag, because tags lie — and each pool slot is a **zero-copy clone** of `MAIN`. A clone takes about two seconds because it copies micro-partition metadata, not data; a session borrows a slot, runs its migrations and tests in isolation, and drops it.
>
> The second version was a rewrite with three ADRs, after the first version taught me that cloning from a shared `PUBLIC` schema is non-deterministic. I hit and fixed real Flyway edge cases — cross-database stream invalidation, which depends on clone order, so I clone the replication DB before the app DB and auto-detect the pattern after a swap; duplicate repeatable migrations; and stub tables for prod-only dependencies. It's what let me run several Claude Code sessions in parallel on the same repo — I think of it as being the tech lead of a team of agents.

---

## S8 · Terraform grant-ownership，7 分钟 RCA（压力下 debug + unblock）

**首答（60 s）**

> A release of our Snowflake infrastructure repo failed in QA: `GRANT OWNERSHIP` on a database was rejected because a reviewer role already held a dependent `USAGE` grant. Someone else was named to investigate; I was cc'd. Seven minutes later I'd posted the root cause — the ownership resource didn't set `outbound_privileges`, so Terraform tried to transfer ownership without revoking dependents — the fix, `outbound_privileges = "REVOKE"`, and a check of the neighboring modules for the same omission. I asked for permission to push, the PR went in, and QA, pre-prod and prod deployed that afternoon.
>
> The senior part is what I found afterward: scanning the whole repo, dozens of ownership resources lack the parameter — most are `future_*` grants where it's harmless — but two in another module are the exact same shape as the one that blew up and haven't fired yet. I flagged them; I'd rather own "here's the next one" than just the one that paged.

---

## S9 · Amex 出款延迟事故（事故指挥 + 领域权威）

**首答（60 s）**

> A large marketplace merchant reported roughly four million dollars of Amex payouts "missing," and a formal incident channel spun up. The incident commander named me one of three engineers who own the fix. Two contributions. First, the SLA: a senior teammate said he didn't have context on US aggregated-Amex SLAs and deferred to me — I established that T+7 is our internal pipeline SLA and that we only disburse after Amex settles funds to us, which separated expected latency from the real regression. Second, the regression itself: an effective-date change made for EU compliance had shifted US disbursement dates by a day. Reverting was the fast option; the robust fix — which I argued for and the group chose — was a region conditional in the table function so EU and US keep independent semantics. Closed in three days.

---

## S10 · 退款费 billing-terms 复盘（推翻自己的结论 + 定量推理 + **SQL**）

**首答（60 s）**

> After a large e-commerce merchant moved to net settlement, some refund fees came out tagged with the old monthly billing terms. My first blast-radius query said about two hundred thousand fee rows across sixty merchants. Before anyone acted on it I re-examined the predicate and found it was wrong: it didn't check that the new pricing schedule existed at fee-creation time — many of those rows had schedules backdated months later and were correct when written. Adding `schedule.created_at <= fee.created_at` took the real scope to about twenty-two thousand rows, thirty merchants, under six thousand dollars.
>
> The root cause was the refund-fee path copying the credit's historical `pricing_schedule_id` instead of resolving the effective schedule at fee time. Along the way I found a second, upstream fragility — a pricing schedule written to the database an hour after the transaction stream had already stamped the day's credits — and showed one fix covers both. I'd rather retract my own number in public than have a remediation sized off a bad predicate.

---

## 追问弹药（任何故事都能接）

| 追问 | 接法 |
|---|---|
| "If volume were 100× larger?" | 剪枝与聚簇（窗口化 `ON`、cluster key 对齐查询模式）→ 拆 warehouse 隔离负载 → 把逐行 UDF 改成 set-based / SQL pushdown（S6 的 Phase 1 就是这个思路）。 |
| "Why Snowflake-native SQL and not Java services?" | 数据在哪，计算就在哪；每步都是事务性 `MERGE`；Java 17 + Gradle + Flyway 做编排、测试与部署——"database-first, Java for orchestration"。 |
| "Biggest risk you took?" | S5 静态拆分数据源：赌的是"事实比运行时判断可靠"，用同源验证把风险买断。 |
| "Who else was involved?" | 永远先说别人做了什么，再说我的决定："I was one of three owners; my piece was…" |
| "What does your team own?" | 亲历 2026-09-17 的好句子："We are the downstream of the downstream — fee calculation and disbursement — so a mistake here is money, not a retry." |
| "How do you work without a PM?" | 亲历 2026-09-17 的好句子："We're engineer-driven: I identify the problem, write the discovery and the ADR, then implement — and I own the on-call for it afterwards." |
| "What did you learn?" | 每个故事的最后一句已经是 learning；追问时换成原则：**fail loudly · same SQL for validation and production · deploy ≠ release · config over code**。 |
