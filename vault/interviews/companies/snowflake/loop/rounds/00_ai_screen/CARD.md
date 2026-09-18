---
title: Chakra CARD · 关键词卡
aliases:
  - Chakra CARD
tags:
  - company/snowflake
  - round/ai-screen
---

# CARD · Chakra 关键词卡（贴摄像头旁 / 手机版）

> 每题只留提示词。全文在 `playbook.md` / 故事笔记 [[S1]]…[[S11]] / `scenarios.md`；题库 `questions.md`。
> 说话规则：**Listening 才开口 · Thinking 闭嘴** · 首答 ≤ 90 s · 每答 = headline → 原语名 → "I decided" → 量级 → learning · 数字都加 "roughly"。
> 必说的 JD 词：**SQL · distributed systems · Java 17 · database internals · large-scale production**。

## 定位（第一行）

**Owns a Snowflake-native settlement & fee platform end to end → wants to build the primitives.** 收尾三词：**ownership · correctness at scale · Snowflake-native**。

## 时间表

- 0–1 开场 → 可问 "how many sections / how long each"
- 1–6 自我介绍 60 s → **[[S1]]** 90 s
- 6–11 场景："Let me structure this…" → clarify → 3 步 → closest thing → trade-off
- 11–16 协作：**[[S5]]** 决策 · **[[S4]]** 跨团队 · **[[S6]]** 说不
- 16–19 反问 ×2 + 表态
- 19–20 三词 + thank you

## 自我介绍（60 s）

- PayPal · Braintree Pricing & Settlement · primary owner of **Snowglobe**
- Snowflake-native: Streams · Tasks · procedures · UDTFs · **Java 17 + Gradle + Flyway** · "database-first"
- ① Amex settlement pipeline end to end · tens of millions txns/yr
- ② config-driven **quality-check + trigger-status** framework · 8 subject areas
- ③ interchange source migration · shadow-validated with the production query · toggle
- side: zero-copy-clone **schema pool** for parallel agent sessions
- NYU MS · intern same team · Kafka event processing
- hook: "heavy consumer of exactly the primitives your teams build"

## [[S1]] · Amex pipeline

- closed-loop network · daily fixed-width file · **good-funds model** · pending table
- `COPY INTO` (file-level dedup) → 6 **append-only Streams** by record type → 6 procedures `SUBSTRING` + `MERGE` composite key → 2 UDTFs `FULL OUTER JOIN` → error log, never drop → Task `AFTER A, B` in one transaction → payout
- decisions: independent offsets · idempotent every stage · one flag isolates the flow · EU extension
- mine: topology → parsers → validators → fee task → kill switch → ~12 hardening PRs · ~1,800-line PR
- broke: late file in yesterday's folder → `PATTERN` all partitions · reject flag → composite key
- change: offsets → config table + generic parsing UDTF
- why not Airflow: locality + transactional MERGE · `STREAM_HAS_DATA` · cost = weaker orchestration → built Streamlit monitor + Datadog

## [[S2]] · Quality-check framework

- contract-config table (subject area, validation, procedure, date col, SLA, JSON params)
- executor: `EXECUTE IMMEDIATE` + `RESULT_SCAN` · PASS/FAIL/WARNING · exception → one bad check never kills the rest
- **trigger-status** → replicated share row → consumers `JOIN STATUS = 'Completed'`
- "insert a config row" instead of a new task · 8 rollouts · used by my interchange migration
- ADR: 50 bad merchants blocked 35k · 4 options · **strictest wins** · sparse failure rows · rejected VARIANT+UDF (pushdown, cell limit)
- status line: designed, reviewed, proven for one subject area, sequenced behind the ramp

## [[S3]] · ACH NULL bug

- my health check paged · forwarded to myself · RCA in minutes
- 100% bank-account · ~200 merchants · ~$10M/day
- `'BT_' || NULL = NULL` → no category → no fee, silently
- shared MERGE used 1-arg UDF overload (no bank branch) → overwrote correct value
- postmortem: control group · time series 0% at every age · 4 reasons e2e missed it
- fix: stopgap → single function w/ default param → versioned `DROP` of legacy · e2e spanning promotion→fee
- principle: **fail loudly** · fix forward + backfill · don't suppress the check

## [[S4]] · AU Amex refund

- PM escalation · 50 replies · 3 teams → routed to me
- data not org chart: ~1M US rows vs 0 AU · ~150 merchants
- `fee_refund_policy = partial` never `full` · config not code · predates migration
- wrote the query so they could verify → thread ended same day → tracked feature

## [[S5]] · Interchange source switch

- transaction view populated after cutoff → miss net-settlement window
- A: smarter fallback (sticky, 3 CTEs) vs **B: static split by fee type + toggle** → "source of truth is a fact"
- discovery: `FULL OUTER JOIN` + `EQUAL_NULL` · >99.9% parity · every diff explained
- pre-cutover: **production query as `count(*)`** · ~14M rows · fraction of a percent
- 4 layers: synthetic key MERGE · **time-windowed ON** · trigger-status JOIN · merchant gate + Amex exclusion
- old task excludes interchange only when toggle on → complementary, never double-count
- toggle off → pre-prod → prod · **deploy ≠ release** · backfill SQL became CDC template

## [[S6]] · Anomaly detector go/no-go

- inherited from departing intern · easy path = keep building
- QA: 6 synthetic merchants vs prod: 18k merchants · 15k plan combos · up to ~760M rows/day
- per-row numpy → would time out · QA could never show it
- dies vs survives → persisted analyst labels first
- Phase 1: consistency rule as **SQL pushdown** · Phase 2: ML rework, 2–3 months, gated
- froze Slack + CI/CD until go · "rather stop than page the team at 3 a.m."

## [[S7]] · schema pool

- shared schema → DDL collisions between branches / agent sessions
- `MAIN` synced to prod-deployed SHA via Deployments API (tags lie) · pool slots = **zero-copy clones** ~2 s
- V2 rewrite + 3 ADRs · Flyway edge cases: cross-DB stream invalidation (clone order) · duplicate repeatables · prod-only stubs
- "tech lead of a team of agents"

## [[S8]] · Terraform 7-minute RCA

- QA release failed · `GRANT OWNERSHIP` rejected, dependent `USAGE` grant
- cc'd not assigned · 7 min: root cause = missing `outbound_privileges` → `"REVOKE"` · checked neighbor modules · asked, pushed PR, QA/pre-prod/prod same afternoon
- after: scanned repo · dozens missing, mostly harmless `future_*` · two real same-shape risks flagged

## [[S9]] · Amex payout incident

- large marketplace merchant · ~$4M "missing" · incident channel · one of three owners
- SLA authority: T+7 internal · disburse only after network settles → expected vs regression
- root: effective-date change for EU shifted US by a day · **region conditional** > revert · closed in 3 days

## [[S10]] · Billing-terms postmortem

- first scope ~200k rows / 60 merchants → predicate missed "schedule existed at fee time"
- corrected: ~22k rows / 30 merchants / < $6k · retracted publicly
- cause: refund path copied historical `pricing_schedule_id` · bonus: 1.5 h creation-lag fragility · one fix covers both

## 场景骨架（每题）

- "Let me structure this: what I'd want to know, how I'd approach it, the closest thing I've done."
- wrong totals → scope by data · walk back · one hypothesis · fix forward + invariant ([[S3]])
- metering / no double-charge → idempotency key upsert · deterministic MERGE agg · separate recon · late = adjustment
- zero-downtime switch → expand · shadow-read · flag · contract ([[S5]])
- slow after deploy → metrics · bisect · profile partitions scanned · per-row→set-based · revert first
- on-call payouts → blast radius + clock · stuck vs late · 15-min update · owner per hypothesis ([[S9]])
- rate limiter → token bucket per (tenant, resource) · atomic decrement · local allowance · exact vs approx
- Kafka exactly-once → effect not delivery · commit after write · MERGE inside DB · replay is a feature
- never read partial data → status row · readiness as JOIN · checks as config · SLA monitor ([[S2]])
- two systems disagree → normalize · FULL OUTER JOIN + EQUAL_NULL · bucket · explain all · daily check ([[S10]])
- scheduler → DAG AFTER A,B · data-triggered · failure budget · backfill = re-enqueue, idempotent
- billions of rows slow → partitions scanned/total · clustering = dominant predicate · skew · window the predicate
- late data → arrival vs effective time · scan all partitions · closed day → adjustment · "expected but not arrived"
- Streams vs Dynamic Tables → imperative control vs pure SELECT + target lag
- zero-copy clone → immutable micro-partitions · pointer list · writes diverge
- cost → per-second, 60-s min · `STREAM_HAS_DATA` gate · cron from upstream readiness · isolated warehouses

## 危险追问

- **$600B** → platform-level; mine = tens of millions txns, billions of dollars
- **repo share** → ~90 PRs; two largest changes are mine; measure by what pipelines process
- **merchant-level shipped?** → framework + 8 rollouts live; merchant-level designed, reviewed, proven for one area, sequenced behind ramp
- **Ruby migration** → Amex logic lived in Rails payout service; my pipeline is the Snowflake-native replacement on the receiving side
- **Sentry** → Datadog + Streamlit + health-check procs; Sentry = app-layer errors
- **Kafka** → gateway events → Kafka → Snowpipe Streaming → Stream/Task; Funding CDC pipeline; intern connector w/ protobuf + poison messages; consumer semantics yes, broker ops = boundary
- **mentor** → newer engineer's exclusion service + schedule sync plug into my domain; I set contracts, review designs vs downstream, fee-calc authority in incidents; re-scoped intern's ML
- **why leave** → owned one platform two years; next is building the primitives
- **level/comp** → fit first; recruiter once team & level known
- **not done X** → "closest thing I've done is Y — here's how I'd approach X"
- **senior?** → design docs, ADRs, on-call, frameworks others onboard onto, mentoring; title follows scope

## 反问

1. next steps + timeline
2. which areas this screen weights for backend
3. 表态：Streams/Tasks/Dynamic Tables scheduling · metering & billing · end-to-end ownership

## 考前 30 分钟

- [ ] Chrome · 关其它 tab / 通知 / Slack / AI 与录屏扩展
- [ ] 单显示器 · 手机移出画面
- [ ] 有线耳机 + 麦 · 预检时开 real-time transcript
- [ ] 插电 + 稳定网络 · 断网立刻回同一链接并回邮件
- [ ] 本卡贴摄像头旁（脸不能长时间离开画面）
- [ ] 面完回复 Ashby 邮件问 Chakra 是否即 "Talent Intake"
