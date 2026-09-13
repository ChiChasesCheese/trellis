# 03 · Chakra 20 分钟剧本（Snowflake · GenSWE / Software Engineer - Backend）

> 通用机制与操作清单在 `../../core/playbooks/ai-voice-screen.md`（先读一遍）。本文件只做一件事：**把 20 分钟按邮件里的四段拆成逐分钟脚本，每段配好英文口述稿**。面试是英文；稿子是英文，注释是中文。
> 打分铁律回顾：Reporter 只读 transcript，每条 expectation 要有「clarity / ownership / structured reasoning / specific examples」的**具体证据**；theoretical = Not Met；没说到 = 0。所以每段都要**说出工具名、决定、数字、我本人做的部分**。

## 0. 一句话定位（贴在摄像头旁的卡片第一行）

> **Backend engineer who owns Braintree's Snowflake-native settlement & fee platform — 22M Amex txns / $138B a year — now wants to build the platform itself.**

三个关键词，收尾时再说一遍：**ownership · correctness at scale · Snowflake-native**。

## 1. 时间表

| 分钟 | 段（邮件原文） | 主答 | 备用追问 |
|---|---|---|---|
| 0–1 | 开场 | 听议程；可问 "How many sections and roughly how long each?" | — |
| 1–6 | Your experience and role-related background | 自我介绍 60 s → 项目深挖 S1（AMEX 管线）90 s | S1 追问版 ×3 |
| 6–11 | Applied scenarios relevant to your role | 用「我做过的最接近的事」答，再讲方法（见 `05-applied-scenarios.md`） | 每题 60–90 s |
| 11–16 | Collaboration and decision-making | S5 shadow-run 决策 90 s；S4 跨团队 60 s；S6 说不 60 s（按它问的挑） | S2 ADR 作为「说服团队」备用 |
| 16–19 | Questions you may have for us | 2 个它能答的 + 1 句表态（见 `06-questions-to-ask.md`） | — |
| 19–20 | 收尾 | 三个关键词 + 感谢 | — |

它会按 allotted duration 主动切段。**任何一段被切走都不要恋战**——没讲完的数字下一段找机会补一句。

## 2. 段一 · 自我介绍（60 秒，English）

> I'm a backend engineer at PayPal, on the Braintree Pricing & Settlement team. For the last year and a half I've been the primary owner of our settlement and fee-calculation platform — internally it's called Snowglobe, and it's built natively on Snowflake: tasks, streams, stored procedures, table functions, all in Java 17 and Snowflake SQL. I'm the top committer on that repo.
>
> Three things sum up my work. First, I designed and built the end-to-end American Express settlement pipeline — file ingestion through fee calculation to payout — which processed about 22 million transactions and 138 billion dollars in 2025. Second, I own the pricing side of our net-settlement migration to Fiserv; I switched our interchange source with a shadow-run reconciliation over 13.7 million rows before rolling it out behind a feature flag. Third, I built a reusable quality-check framework the team has reused about eight times, and wrote the ADR that fixed a flaw in my own first design.
>
> Before that I did my master's in CS at NYU and interned on the same team, building Kafka-based transaction-event processing on Kubernetes.
>
> I'm interested in Snowflake because I've spent two years as a very heavy user of exactly the primitives your backend teams build — Streams, Tasks, MERGE semantics, task scheduling, warehouse cost — and I want to work on the platform side of that.

中文注释：
- 数字全部来自 evidence-base 已确认项（$138.6B / 21.96M / 13.7M 行 / ~8 次复用）。**不要说 $600B**——那是简历口径未闭合的数字；如果它读到简历追问 "$600B"，答法见 §5。
- "top committer" 是真实的（615 commits，#1）。
- 最后一句是 hook，引它去问「你用 Snowflake 做了什么」——这正是你最强的地方。

## 3. 段一 · 项目深挖 S1（90 秒首答 + 追问版）

**首答（headline → mechanism → number → learning）**

> The project I'd pick is the American Express integration. Amex is a closed-loop network — instead of interchange files it sends us a proprietary fixed-width settlement file every day, called GRRCN. I owned the pipeline end to end.
>
> Mechanically: a scheduled Snowflake task copies the file from S3 into a staging table with the whole line as one column; six append-only streams fan the rows out by record type; stored procedures parse the fixed-width fields with SUBSTRING and TRY_CAST and MERGE them into six raw tables — transactions, pricing, fee revenue, adjustments, chargebacks, summary; a table function validates and consolidates them into our canonical transactions table; and a downstream task computes the Braintree interchange fee per transaction and hands aggregates to the Funding service for payout. I also migrated the legacy Ruby script that did part of this into Snowflake-native SQL.
>
> The hard part was correctness under partial files and retries, so every stage is idempotent through MERGE keys, and one feature flag can stop the whole flow. It's been in production about 18 months; in 2025 it processed roughly 22 million transactions, about 138 billion dollars.
>
> What I'd do differently: build the quality gates at merchant granularity from day one — which is what I later did as a separate framework.

**追问 1 · "What was *your* specific contribution?"**

> I inherited a stub from a previous engineer and everything from the design onward is mine: the task-and-stream topology, the seven staging and target tables, the parsing UDTFs, the feature-flag kill switch, the EU extension, and about ten hardening PRs over the following year. The single largest PR in my tenure — around 1,800 lines — is this pipeline.

**追问 2 · "Why streams and tasks instead of an external orchestrator?"**

> Two reasons. Data locality — the file lands in Snowflake anyway, and keeping parse-validate-compute inside the warehouse means no data leaves and every step is a transactional MERGE. And operational simplicity — `SYSTEM$STREAM_HAS_DATA` gates each task, so nothing runs on empty input and backfills are just re-enqueuing rows into the staging table. The trade-off is weaker observability than Airflow gives you, which is why I built a Streamlit task monitor and Datadog alerts on top.

**追问 3 · "How did you validate correctness?"**

> Three layers. Row-level: TRY_CAST and TRY_TO_DATE so a bad field never aborts a batch, and rejected rows are kept, not dropped. Batch-level: the quality-check framework asserts counts and sums per subject area before downstream reads. And reconciliation: the fee totals are reconciled against what Amex reports in the summary record type. When those disagree, the task halts and pages me.

## 4. 段三 · 协作与决策（三选二，按它问的挑）

**S5 · 一个技术决策及其 trade-off（90 秒）**

> Braintree is moving large merchants to direct Fiserv net settlement — the merchant receives funds T+1 and Braintree stops fronting interchange, which was on the order of 450 million dollars a month of float. I own the pricing side.
>
> The decision was switching our interchange source of truth from the transaction view to the settle view. Option A was flip it and monitor. Option B was a shadow run first. I chose B because fees are revenue — a silent regression is a P1. I wrote a day-level shadow reconciliation comparing both sources: 13.7 million rows, over 99.9% field agreement, 0.224% variance, and every discrepancy category explained before we moved. Then rolled out merchant by merchant behind a feature toggle.
>
> The cost was about two extra weeks. The payoff: zero fee regressions, and the shadow-run SQL became a reusable backfill template the team now uses for any CDC cutover. It's the prerequisite for roughly 55 billion dollars of incremental volume.

**S4 · 跨团队协作（60 秒）**

> A product manager escalated through our formal help process: Australian merchants weren't seeing Amex refund fees. The thread had about fifty replies across three teams before it was routed to me. I pulled the data: over a million refund-fee rows in the US, zero in Australia, across 157 merchants. Root cause was a config assumption — every AU merchant had `fee_refund_policy = partial`, and the fee logic only fired on `full`. I wrote up the finding with the exact query so the PM and the other team could verify it themselves, and it became a tracked fix. What made it work was giving everyone the same evidence instead of arguing about ownership.

**S6 · 我说了不 / 推迟投入（60 秒）**

> I inherited an ML fee-anomaly detector from an intern who was leaving. The easy path was to keep building. Instead I wrote a go/no-go gate: QA had run on 834 million rows and six synthetic merchants; production is 39 billion rows and 18,000 merchants, and per-row numpy serving at 760 million rows a day would almost certainly time out. I proposed a phased cutover and froze the CI/CD and Slack-alert work until the gate said go. That's "Get It Done" for me — results matter, so I'd rather stop a project than ship one that pages the team at 3 a.m.

**S2 · 说服团队改方案（备用，60 秒）**

> I found a flaw in a framework I had built myself: one subject area failing 4% of checks blocked every merchant. I wrote a formal ADR — MADR format, with a correctness argument and three rejected alternatives — proposing merchant-level granularity. Writing down the rejected options is what got it accepted quickly: reviewers could see I had considered their objection already.

## 5. 危险追问与答法

| 追问 | 答法 |
|---|---|
| "Your resume says $600B+" | "That's the platform-level annual volume the pipeline sits in. The number I personally stand behind for the Amex pipeline is 138 billion in 2025 — from our impact summary." |
| "Sentry?" | 主讲 Datadog：alert routing、task monitor；Sentry 只说 "for error tracking on the ingestion layer"。不展开。 |
| "Kafka in Kubernetes" (intern) | 讲真实的：Kafka-to-Snowflake connector + protobuf converter + poison-message 隔离；K8s 是 connector 跑的地方。不说 "我搭了 Kafka 集群"。 |
| "Did you mentor anyone?" | domain-ownership 框定：Ziyang 的 exclusion service / gRPC journaling sync 全部接入我拥有的领域，我定 contract、在事故里是他依赖的权威。**不编 PR review 细节。** |
| "Why leave PayPal?" | "I've owned one platform end to end for two years; the next step in depth is to build the primitives I've been consuming." 不抱怨。 |
| "Level / comp?" | "I'm focused on fit at this stage; happy to discuss with the recruiter once we know the team and level." |
| 它问的场景我没做过 | 先说最接近的真实经验，再给方法："I haven't built X, but the closest thing I've done is Y — and here's how I'd approach X." |

## 6. 收尾（20 秒）

> To sum up: I bring end-to-end ownership of a Snowflake-native settlement platform, a track record of getting correctness right at the 100-billion-dollar scale, and I want to move from consuming these primitives to building them. Thank you — I'm looking forward to the next conversation with the team.

## 7. 前一晚 / 当天

- 前一晚：`07-mock.md` 跑两遍（一遍看稿，一遍不看稿只看关键词卡）；每个故事录音 90 秒回听——检查是否有 headline / number。
- 当天：`../../core/playbooks/ai-voice-screen.md` §4 清单逐项打勾；用 **Chrome**；关键词卡贴摄像头旁；开 real-time transcript。
- 面完：把实际被问的题写进 `02-process.md` 末尾「亲历」节。
