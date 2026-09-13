
# CARD · Snowflake Chakra 20 分钟浓缩卡

> [!tldr]
> - 岗位：**GenSWE**（Snowflake 官方早期职业通道，统一 loop → team matching），Ashby 标题 Software Engineer - Backend。1.5 年经验大概率 IC1（Bay Area 中位 TC ≈ $236K）。
> - 这轮：Chakra（HackerRank AI）**20 分钟语音**，开摄像头 + 全屏共享 + **单显示器**，左侧实时转录。一手报告 ×3：**只问 BQ + 项目，无 coding**。人看记录后决定。
> - 打分只认 transcript：每条 expectation 要有「clarity / ownership / structured reasoning / specific examples」；**theoretical = Not Met；没说到 = 0**。
> - 每答：headline → mechanism → number → learning，首答 60–90 s，留追问空间。
> - **不说 $600B**；说 138B / 22M / 13.7M rows / 0.224%。
> - 这是 `03-chakra-playbook.md` 的浓缩版：只留时间表、英文稿、危险追问、考前清单，适合手机或贴在摄像头旁。

## 时间表

- 0–1 开场：可问 "How many sections and roughly how long each?"
- 1–6 经历：自我介绍 60 s → S1 AMEX 管线 90 s
- 6–11 场景：用做过的最接近的事答，再讲方法
- 11–16 协作 / 决策：S5 shadow-run · S4 跨团队 · S6 说不
- 16–19 反问：2 个它能答的 + 1 句表态
- 19–20 收尾：三个关键词

看到 **Thinking** 闭嘴等；**Listening** 才开口。沉默用 "Let me think about that for a second — the key decision there was…" 填。

## 自我介绍（60 s）

> I'm a backend engineer at PayPal, on the Braintree Pricing & Settlement team. For the last year and a half I've been the primary owner of our settlement and fee-calculation platform — internally it's called Snowglobe, and it's built natively on Snowflake: tasks, streams, stored procedures, table functions, all in Java 17 and Snowflake SQL. I'm the top committer on that repo.
>
> Three things sum up my work. First, I designed and built the end-to-end American Express settlement pipeline — file ingestion through fee calculation to payout — which processed about 22 million transactions and 138 billion dollars in 2025. Second, I own the pricing side of our net-settlement migration to Fiserv; I switched our interchange source with a shadow-run reconciliation over 13.7 million rows before rolling it out behind a feature flag. Third, I built a reusable quality-check framework the team has reused about eight times, and wrote the ADR that fixed a flaw in my own first design.
>
> Before that I did my master's in CS at NYU and interned on the same team, building Kafka-based transaction-event processing on Kubernetes.
>
> I'm interested in Snowflake because I've spent two years as a very heavy user of exactly the primitives your backend teams build — Streams, Tasks, MERGE semantics, task scheduling, warehouse cost — and I want to work on the platform side of that.

## S1 · 项目深挖（90 s）

> The project I'd pick is the American Express integration. Amex is a closed-loop network — instead of interchange files it sends us a proprietary fixed-width settlement file every day, called GRRCN. I owned the pipeline end to end.
>
> A scheduled Snowflake task copies the file from S3 into a staging table; six append-only streams fan the rows out by record type; stored procedures parse the fixed-width fields with SUBSTRING and TRY_CAST and MERGE them into six raw tables; a table function validates and consolidates them into our canonical transactions table; and a downstream task computes the Braintree interchange fee per transaction and hands aggregates to Funding for payout. I also migrated the legacy Ruby script into Snowflake-native SQL.
>
> The hard part was correctness under partial files and retries, so every stage is idempotent through MERGE keys, and one feature flag can stop the whole flow. In production about 18 months; in 2025 roughly 22 million transactions, about 138 billion dollars.
>
> What I'd do differently: build the quality gates at merchant granularity from day one — which is what I later did as a separate framework.

> [!example]- 追问版
> - **Your specific contribution?** Inherited a stub; everything from design onward is mine: task/stream topology, seven tables, parsing UDTFs, the kill switch, EU extension, ~10 hardening PRs; the largest PR in my tenure (~1,800 lines).
> - **Why streams/tasks, not Airflow?** Data locality + every step a transactional MERGE; `SYSTEM$STREAM_HAS_DATA` gates tasks so nothing runs on empty input. Trade-off: weaker observability — so I built a Streamlit monitor + Datadog alerts.
> - **How did you validate?** Row-level TRY_CAST keeps bad rows instead of aborting; batch-level quality checks on counts/sums; reconciliation against Amex's own summary record — mismatch halts the task and pages me.

## S5 · 决策 + trade-off（90 s）

> Braintree is moving large merchants to direct Fiserv net settlement — funds T+1 and Braintree stops fronting interchange, about 450 million dollars a month of float. I own the pricing side.
>
> The decision: switch our interchange source of truth from the transaction view to the settle view. Option A, flip and monitor. Option B, shadow run first. I chose B because fees are revenue — a silent regression is a P1. Day-level shadow reconciliation: 13.7 million rows, over 99.9% agreement, 0.224% variance, every discrepancy explained. Then merchant by merchant behind a feature toggle.
>
> Cost: two extra weeks. Payoff: zero fee regressions, and the SQL became the team's reusable backfill template. It's the prerequisite for roughly 55 billion dollars of incremental volume.

## S4 · 跨团队（60 s）

> A PM escalated through our formal help process: Australian merchants weren't seeing Amex refund fees — a fifty-reply thread across three teams before it reached me. I pulled the data: over a million refund-fee rows in the US, zero in Australia, across 157 merchants. Root cause: every AU merchant had `fee_refund_policy = partial` and the logic only fired on `full`. I wrote it up with the exact query so the PM and the other team could verify it themselves. Giving everyone the same evidence beat arguing about ownership.

## S6 · 说不（60 s）

> I inherited an ML fee-anomaly detector from a departing intern. The easy path was to keep building. Instead I wrote a go/no-go gate: QA had run on 834 million rows and six synthetic merchants; production is 39 billion rows and 18,000 merchants, and per-row numpy serving at 760 million rows a day would almost certainly time out. I proposed a phased cutover and froze further work until the gate said go. Results matter — I'd rather stop a project than ship one that pages the team at 3 a.m.

## S3 · 最难的 bug（备用，60 s）

> A PagerDuty fired: some transactions had no Braintree fee. Scoping showed 100% standard ACH — about 196 merchants, 11 million dollars a day. The fee-category key was `'BT_' || sub_kind`, sub_kind was NULL for that population, and NULL concatenation yields NULL, so no fee row was generated. Root cause: a new two-argument UDF overload while the promotion path still called the one-argument version. Fixed, backfilled, consolidated the overloads, added a non-null assertion to our quality checks.

## 场景题骨架

每题："Let me structure this: what I'd want to know, how I'd approach it, then the closest thing I've actually done." → Clarify 1 句 → 3 步 → 真实例子 + 数字 → trade-off 1 句。

- 管线算错 → S3 的方法（scope by data → walk back stages → one hypothesis → fix forward + backfill + new check）
- 计量不重复计费 → idempotency key upsert → deterministic MERGE aggregation → separate reconciliation；late events as next-cycle adjustment
- 无停机 schema / source 切换 → expand → shadow-read → flag by cohort → contract（S5）
- 变慢 → metrics first, bisect the deploy, read the plan; revert before debugging live
- on-call 伙伴出款延迟 → blast radius + clock, stuck vs late, 15-min interim update, owners per hypothesis（S9 SLA）
- 多服务共用 quota → token bucket per (tenant, resource) in shared store with atomic decrement; local allowance to avoid hot key

## 危险追问

- **$600B on resume** → "That's the platform-level annual volume the pipeline sits in. The number I personally stand behind for the Amex pipeline is 138 billion in 2025."
- **Sentry** → 主讲 Datadog；Sentry 只说 error tracking on the ingestion layer。
- **Mentoring** → domain-ownership 框定（Ziyang 的 exclusion service / gRPC sync 接入我拥有的领域，我定 contract）；不编 1:1 细节。
- **Why leave PayPal** → "owned one platform end to end for two years; next step is building the primitives I've been consuming."
- **Level / comp** → "focused on fit at this stage; happy to discuss with the recruiter once we know the team."

## 反问（对 AI）

1. "What are the next steps after this screen, and roughly when would I hear back?"
2. "Which areas does this screen weight most heavily?"
3. 表态："One thing I'd like to ask the team next round: how the tasks and dynamic-tables scheduling side is organized, and whether the metering and billing pipeline is somewhere an early-career engineer can own something end to end."

## 收尾（20 s）

> To sum up: end-to-end ownership of a Snowflake-native settlement platform, a track record of getting correctness right at the 100-billion-dollar scale, and I want to move from consuming these primitives to building them. Thank you.

## 考前 30 分钟

- [ ] Chrome；关其它 tab / 通知 / Slack / AI 与录屏扩展
- [ ] 单显示器；手机移出画面
- [ ] 有线耳机 + 麦；预检时**打开 real-time transcript**
- [ ] 插电 + 稳定网络；断网立刻回同一链接并邮件 recruiter
- [ ] 关键词卡贴摄像头旁（脸不能长时间离开画面）
- [ ] 做完后回复 Ashby 邮件问：Chakra 是否就是 "Talent Intake"，还是还有第二环节
