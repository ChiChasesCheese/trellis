# 行为题和 HM 题库：Global Payment（46 题）

- 支付组的简历拷问把你的 PayPal 经历当**领域知识**来考：费用算没算对、结算是否幂等、对账差异怎么查、事故怎么处理、重试下钱是否正确。这些在 **F 组**（Q38–Q46），每一场技术面都可能被问到，先练它们。
- 每题：用哪个故事 · 时长 · 3–4 条可直接说出口的要点（加粗是路标）· 2–4 个追问和一行回答要点。
- 先讲 L1，停，等追问。故事要 60–90 秒讲完，最长 2 分钟。
- 【待补：…】 补完前不要口播；每题给了补不出来时的诚实降级。
- 要点用英文，因为面试默认英文；HM 若换普通话，技术名词仍用英文原词。

## 故事一览

- 故事文件（口述提纲和逐字稿）：
  - [[S1_settlement-pipeline-never-drop-bad-data|S1 Amex 结算管线]] · [[S2|S2 质量检查框架]] · [[S3_silent-null-root-cause|S3 无声的 NULL]] · [[S4|S4 AU Amex 退款费]]
  - [[S5_cutover-with-the-production-query|S5 interchange 数据源切换]] · [[S6_per-row-cost-times-peak-rows|S6 异常检测 go/no-go]] · [[S7_schema-pool-and-why-a-clone-is-fast|S7 schema pool]]
  - [[S8_fix-one-then-scan-the-repo|S8 修一个再扫仓库]] · [[S9|S9 出款延迟事故]] · [[S10_retract-own-number|S10 撤回自己的数字]] · [[S11|S11 实习期 Kafka]] · [[R1_quant-stroller-research-platform|R1 Quant-Stroller]]

| 故事 | 一句话 | 只说这些数字 |
|---|---|---|
| S1 | 结算管线：出错就记下来，绝不丢 | 约 22M 笔 / 半年；18 个月生产；最大单个 PR 约 1,800 行 |
| S2 | 配置驱动的质量检查 + 「数据可读」信号 | 8 个领域铺开；约 50 个坏商户挡住 35,000 个 |
| S3 | 没有报错的 bug：NULL 传播 | 约 200 个商户；4 个测试漏洞；2 个重载 → 1 个函数 |
| S4 | 用一条查询结束 50 条回复 | 1,079,627 行 vs 0；157 个澳洲商户 |
| S5 | 用生产查询本身做验证的数据源切换 | 13.7M 行；>99.9% 一致；行数差 +0.224% |
| S6 | 上线前用规模估算叫停 | 6 个合成商户 vs 约 18,000；峰值一天最多约 760M 行 |
| S7 | 没人要的工具：schema pool | 约 2 秒克隆；3 篇 ADR |
| S8 | 修一个，再扫整个仓库 | 7 分钟；79 个里 42 个缺参数 |
| S9 | 事故指挥里当领域权威 | 约 $4M 出款「不见了」；三位 fix owner 之一 |
| S10 | 公开撤回自己的数字 | 196,274 → 21,923 行；61 → 30 商户；$11,123 → $5,854.52 |
| S11 | 实习期 Kafka 消费侧幂等 | 并行度 = replicas × tasks.max，上限是分区数 |
| R1 | 个人研究平台（不是雇主的工作） | 340+ 次实验；470+ 测试文件 |

| 问题类型 | 首选故事 | 备选 |
|---|---|---|
| 自我介绍 / 简历 | S1 | S5、S11 |
| 最有影响的项目 / 数据管线 | S1 | S5 |
| 选型、规模、schema | S1、S5 | S2 |
| 性能 | S6（容量推理） | S5 的窗口化 |
| 事故 / 稳定性 | S3 | S9、S8 |
| 分歧 / 沟通 | S4 | S3、S9 |
| 失败 / 错误 | S10 | S8 |
| 模糊 / 接手 | S6 | S4 |
| 自发做的事 | S7 | S8 |
| 指标 / 实验 | S10 | S5 |
| AI 使用 | S7 | S6 |
| 费用计算的正确性 | S10 | S3、S4、S1 |
| 结算幂等 / 重试下的钱 | S1 | S5、S11 |
| 对账差异 | S1 | S5、S3 |
| on-call 事故 | S3 | S9 |
| 资金流与出款时效 | S9 | S1 |
| 退款、拒付、多币种 | S4 | S10、S1 |

## A · 开场与动机

### Q1 · Tell me about yourself（≤ 60 秒）· S1 → S5
**Hook：「I'm a backend engineer on PayPal's Braintree fee platform, and what I'm best at is making money pipelines correct and provable.」**
- **Who**: about **twenty months** full time after an **internship** on the same team; Java, Python, SQL; **Snowflake**, **PostgreSQL**, **Kafka**.
- **Flagship**: I **built** the **Amex settlement pipeline** from a stub, about **22M transactions** in half a year, and I owned the **interchange-fee track** of the net-settlement program: **13.7M rows** cut over at **>99.9%** parity.
- **How I work**: every stage **idempotent**, bad data **recorded, never dropped**, validate with the **production query itself**; I'm the **on-call owner** who root-causes quiet data bugs.
- **Why here**: 【待补：为什么是 Global Payment，一句话；建议落在「我已经在做钱的正确性，想在多市场、多币种、消费金融的规模上做」】
- **Follow-ups**:
  - **Which part was yours?** Everything from the **topology** of the Amex pipeline onward; at the program level I owned the **fee side**, not the whole program.
  - **What's your stack?** **Java, Python, SQL**; Snowflake and PostgreSQL daily; Kafka from my internship.
  - **Do you know Go?** Say it straight: 【待补：真实的 Go 经验】; if none, "My production languages are Java and Python; I can learn Go on the job."

### Q2 · Walk me through your resume · S1 · 3 分钟
- **PayPal full time**: Amex pipeline (**~22M transactions**, **18 months** live) → **net-settlement interchange track** (**13.7M rows**) → **quality-check framework** rolled out to **8 areas** → **on-call** and observability.
- **Internship**: Kotlin/Spring service, **Kafka** consumers into the warehouse, **Spark + Airflow** validators.
- **Education**: **NYU MS CS** after a **construction-management BS**; "I switched into CS for my master's and have been writing production code since."
- **After each block, stop**: "I can go deeper on the pipeline or the cutover."
- **Follow-ups**:
  - **Go deeper on the pipeline.** Stop after L1; offer S1 or S5 and wait.
  - **What did the internship teach?** Consumer-side **idempotency**: dedup before insert, unique constraint as the backstop; parallelism = **replicas × tasks.max**, capped by **partition count**.
  - **Why the switch into CS?** One sentence; then back to the work.

### Q3 · Why ByteDance Global Payment, and why this team? · 45 秒
- **A concrete engineering problem**: one payment platform behind **TikTok Shop, LIVE, ads and subscriptions** in many markets: pay-in, pay-out, **FX**, **reconciliation**; the team I'd join builds **consumer finance** on top (**PayLater**, credit, wallet).
- **Tie to me**: at PayPal I own **fee calculation and settlement** correctness: the Amex pipeline (**~22M transactions**) and the interchange cutover (**13.7M rows**, **>99.9%** parity). The same problems, **more markets, more currencies, more products**.
- **Public facts only**: the posting lists acquisitions, disbursements, transaction monitoring, payment-method management, FX, accounting, reconciliation; claim nothing beyond it.
- 【待补：你个人真正的原因，一句话】
- **Follow-ups**:
  - **What do you know about the team?** Only what is public: **Global Payment** serves ByteDance platforms outside China; **Financial Product and Solution** builds **PayLater, credit, insurance and wallet** products, mostly for markets outside the US.
  - **Have you used TikTok Shop or TikTok Pay?** 【待补：你自己的真实使用和一个具体观察，例如结账或退款体验】
  - **Why consumer finance, not core payments?** It's the same ledger underneath: a loan is a **receivable** with a **schedule**; correctness and reconciliation carry over, and the **credit and interest** side is what I want to learn.

### Q4 · Why are you leaving PayPal? · 30 秒
- **Forward-looking**: **many markets and currencies**, a payment platform used by several large products, and **new product lines** (consumer finance) rather than one mature fee system.
- **Credit the place**: "I owned a **money pipeline end to end** and learned on-call and root-causing there."
- **Never** badmouth people or process; salary is never the reason.
- 【待补：真实原因，一句话；签证、地点、团队变化也说真话，简短，然后转向「what I want next」】
- **Follow-ups**:
  - **What did you like least there?** Say what you **want next**, not what you disliked.
  - **Would you stay for a promotion?** 【待补：真实情况】

### Q5 · You've done fees and settlement; this team builds PayLater and credit. What transfers, what's new? · 45 秒
- **Transfers directly**: **idempotent** pipelines, **reconciliation** against an independent source, **effective-dated pricing** (S10: resolve the schedule **at fee time**), on-call for a money path.
- **Evidence**: S10 (**196,274 → 21,923** rows, retracted in public) and S5 (**>99.9%** field parity before cutover).
- **New to me, said plainly**: **credit decisioning**, **interest accrual**, **delinquency** (days past due, collections); "I know the mechanics; I haven't owned a lending system."
- **How I'd ramp**: learn the **loan state machine** and the **ledger postings** for disbursement, accrual and repayment first, then the risk side.
- **Follow-ups**:
  - **How would you generate an instalment schedule?** Integer minor units; due dates from the **start date + k months**; the **last instalment absorbs rounding**; principal sums exactly (see [[07-class-design]]).
  - **What's hard about interest accrual?** **Daily accrual, monthly posting**; one rounding rule; the **repayment waterfall** (fees → interest → principal) must be auditable.
  - **What would you learn first?** The team's **ledger model** and how a loan is **reconciled** against the funding partner.

### Q6 · Where do you want to be in 2–3 years? · 30 秒
- **Own a system** end to end at a larger scale, and be the person who **sets the bar** on correctness.
- **Grow others**: contracts and design reviews for newer engineers.
- **Year one**: learn the stack (**Go**, the team's RPC and data platforms) and ship something with **measured impact**.
- **Follow-ups**:
  - **Staff track or manager?** 【待补：你的偏好】
  - **What would you ship in year one?** A **small, measurable** change that proves you understand the team's metrics.

### Q7 · What level are you targeting, and what scope have you owned? · 45 秒
- **Scope**: S1 from **stub to 18 months** in production; S5 the **fee side** of a multi-quarter program; S2 a **framework** other engineers onboard onto.
- **Decisions that are mine**: S5 **static split** over a smarter fallback; S2 ADR with **four alternatives** and a **"strictest wins"** safety argument.
- **Metrics**: **22M** transactions, **13.7M** rows at **>99.9%**, **~50 bad merchants blocking 35,000**.
- **Boundary**: "I owned the **fee side** of net settlement; the program owner of record is someone else."
- **Follow-ups**:
  - **Have you led other engineers?** A newer engineer's **three pieces** plug into my platform; I defined the **contracts first**. See Q31.
  - **What would a 2-2 do that you haven't?** 【待补：你自己对差距的诚实判断，一句话，加你的补救计划】
  - **You have about two years; why 2-2?** "Judge me on **scope and decisions**, not years: I owned a settlement pipeline **end to end** and a **cutover** in a revenue path. I'd like the **design round** to show it."

## B · 项目与技术深度

### Q8 · Your highest-impact project: why that architecture, what proved success, what would you change? · S1 · 2 分钟
- **Why it matters**: Amex is **closed-loop**: one **fixed-width file a day**; we can't book a transaction until the file confirms it **settled**.
- **Architecture**: `COPY INTO` a staging table → **six append-only streams** (one per record type, each with its own **offset**) → procedures `MERGE` on a **composite key** → two validators with a **full outer join**; mismatches go to an **error log**, never dropped → fee task in **one transaction**.
- **Proof**: **three layers**: row (`TRY_TO_DECIMAL`, a bad field doesn't kill the batch), batch (health checks), **reconciliation** against Amex's own summary record; a mismatch **halts** and **pages** on-call.
- **What I'd change**: the six parsers repeat one **offset table**; use a **config table + one generic parser**.
- **Follow-ups**:
  - **Why not Airflow or Spark?** **Data locality** and **transactional** steps in the warehouse; the cost is **weaker orchestration**, so I built monitoring on top.
  - **Exactly-once?** No; **at-least-once plus idempotent writes** is effectively once.
  - **What exactly was yours?** Everything from the **topology** onward, about a dozen hardening PRs; the largest single PR was this pipeline.
  - **What broke in production?** A file landed in **yesterday's folder**; I scan **all date partitions** by pattern and rely on **load history** for dedup.

### Q9 · Walk me through a data pipeline you built · S1（+ S11）· 2 分钟
- **Flow in six steps**: file lands → `COPY INTO` staging → streams by record type → parse and `MERGE` → validate against pending → fee calculation → aggregates to payouts.
- **Gating**: `SYSTEM$STREAM_HAS_DATA` so a warehouse **never spins up on empty input**.
- **Failure handling**: late files, a **reject** that arrives after a **settled** record (both coexist; the validator decides), two upstream tasks **out of step** (error logged, **self-heals** next run).
- **Kafka side (internship)**: consumers book **idempotently**; a poison message returns a **null record** instead of killing the task.
- **Follow-ups**:
  - **How do you monitor it?** A task monitor and **Datadog** alerts driven by health-check procedures. 【待补：stream 过期的实际监控】
  - **Two upstream tasks out of step?** `AFTER A, B` guarantees each ran, **not on the same batch**; mismatches go to the error log and self-heal.
  - **What would make it streaming?** Amex sends a **daily file**, so batch fits; with a real-time source I'd consume a log with partitioning. I haven't operated that.

### Q10 · A scaling decision you made · S5 / S1 / S6 · 60 秒
- **S5**: staging only grows, so an equality `ON` scans **all history**; a **one-month window** lets **zone maps prune** and keeps scan cost **constant**; the cost is a dedup **blind spot** past a month, **documented beside the clause**.
- **S1**: **separate streams** so consumers don't block each other; **gating** so nothing runs on empty input.
- **S6**: ask **per-row cost × peak rows** before writing the serving path; do **set-based** work **where the data lives**.
- **Follow-ups**:
  - **How would it handle 100× the data?** I'd **measure time per stage and rows per second** first; then partition by day and make the heavy step incremental. Reasoning, not something I ran.
  - **How do you know pruning worked?** I'd read the **query profile** (partitions scanned vs total). 【待补：是否真的看过；没有就说「I reasoned it from the clustering」】

### Q11 · A performance problem you found and fixed · S6 / S5 · 60–90 秒
> 先说：**my clearest example is capacity reasoning, not profiling a running system.**
- **S6 (before launch)**: an inherited anomaly detector had **only run on 6 synthetic merchants**; production is **~18,000 merchants**, up to **760M rows** a day; the design was a **per-row** forward pass; the arithmetic said it would **time out**.
- **Action**: Phase 1 = the deterministic rule as **set-based SQL** in the warehouse; Phase 2 = retrain and redesign inference **behind a go/no-go gate**.
- **If it had been live**: measure **per-row latency at small N**, separate **CPU from data movement**, extrapolate.
- 【待补：一个真实的剖析故事：现象 + 一个数字，怎么测，根因在哪一层，前后对比，回归测试】
- **Follow-ups**:
  - **Did you profile it?** **No**; it never ran at scale. Never say "I made it N× faster".
  - **Why is per-row slow here?** Per-row **call overhead** and **data movement** out of the warehouse; a set-based query does **one scan** in place.
  - **Is pushdown always faster?** Only if the logic is **expressible set-wise** and the data is already there.

### Q12 · Defend the schema, the keys and the concurrency model · S1 / S5 · 2 分钟
- **Keys**: S1 **composite key** = reference number + **reject indicator**, so a settled and a rejected record **coexist**; S5 **synthetic key** = prefix + invoice number, so an hourly re-run is a **no-op**.
- **No secondary indexes in Snowflake**: pruning comes from **micro-partition metadata (zone maps)**, hence the **windowed `ON`**.
- **Concurrency**: **independent offsets** per stream; streams aren't transactional with the writes, so correctness comes from the **downstream `MERGE` key**; the fee task runs in **one explicit transaction**.
- **System of record**: pricing schedules live in **PostgreSQL** (**unique constraints**, atomic header + N fee rows); Snowflake is where we **aggregate**.
- **Follow-ups**:
  - **Two writers, same key?** The `MERGE` key makes the second a **no-op**; conflicts across systems surface as `FAILED_PRECONDITION`.
  - **Why a composite key?** Without the reject indicator, a later reject would **overwrite** the settled record.
  - **What does a stale stream do?** It goes **silent if unconsumed**. 【待补：你实际怎么监控】

### Q13 · A migration with no downtime · S5 · 90 秒
- **Choice**: **static split by fee type** over a smarter fallback; "in a revenue path the **source of truth** should be a **fact**, not a runtime decision."
- **Validation**: **full outer join** with `EQUAL_NULL` field by field: **>99.9%**, every difference explained; then the **production query itself** as `count(*)` on a full day: **+0.224%**.
- **Release**: **toggle off by default**; pre-prod, then production; **deploy and release are separate steps**.
- **No double counting**: the old task **skips interchange** when the toggle is on; **source filtering**, not `MERGE` dedup, makes the two paths exclusive.
- **Follow-ups**:
  - **Why not dual-write?** Two tasks gated in **opposite directions** by one toggle *are* the exclusion; dual-write without it **double-charges**.
  - **How do you roll back?** Flip the toggle: a **fast off**. 【待补：是否真的用过】
  - **What can still go wrong?** Reprocessing **past the window**; one-sided same-day records arrive later.
  - **0.07% vs 0.224%?** Two **different** numbers: field-level mismatch vs row-count difference.

### Q14 · An architectural disagreement settled with data · S5 / S3 / S2 · 60 秒
- **S5**: option A (smarter fallback) vs B (static split); I chose B on **sticky state and three CTEs**, and showed it with the **parity run**. 【待补：有没有资深同事倾向 A】
- **S3**: someone suggested adding ACH to the check's **exclusion list**; I wrote the **numbers** down; it would turn a **loud** detector **silent**; the check stayed.
- **S2**: an ADR with **four alternatives**; chose the one that kept **predicate pushdown**, with a **"strictest wins"** safety argument.
- **Method**: **evidence anyone can re-run**, not opinion.
- **Follow-ups**:
  - **What if you'd lost?** See Q22.
  - **How did you present the alternatives?** Four options, each with its **read-side cost**, one chosen with a **correctness argument**.

### Q15 · Something you built that nobody asked for / over-engineering · S7 · 60 秒
> 先说：**it's my personal repo, not the team toolchain.**
- **No ticket, no owner**: tests shared one schema; two engineers or **two AI sessions** collided on DDL.
- **V1 → V2**: V1 depended on **who migrated last**; V2 derives from the **deployed commit**; slots are **zero-copy clones** (~**2 seconds**).
- **Restraint**: three **ADRs**, one records what I **deliberately did not fix**.
- **Follow-ups**:
  - **Isn't that over-engineering?** I cut it to the **one failure** I could name; the ADR lists what I **left out**.
  - **Why is a clone 2 seconds?** **Immutable micro-partitions + metadata pointers**; no data copied.
  - **Two sessions grab the same slot?** 【待补：真实的借用 / 归还机制】

### Q16 · A win for other engineers' (or users') experience · S2 / S7 · 45 秒
- **S2**: "is this data safe to read" went from a **Slack convention** to a **`JOIN` condition**; adding a check = **insert a config row**, no release.
- **S7**: several agent sessions run **migrations and tests concurrently** without colliding.
- **Measure**: 【待补：采用人数或节省时间；没有就说「I don't have a number; the evidence is that other teams adopted it」】
- **Follow-ups**:
  - **Who used it?** S7 on-call copilot: **adjacent teams adopted it**. 【待补：人数】
  - **What was the cost?** S2 dynamic SQL loses **static checking**; a config typo fails at **runtime**.

## C · 稳定性与事故

### Q17 · Most memorable production incident · S3 · 90 秒
**Hook：「My hardest bug threw no error: rows that should exist were simply missing.」**
- **Detect**: a daily check **I built** said some settled transactions had **no fee**: about **200 merchants**.
- **Method**: **slice** the missing rows → one payment type → **one row** with `sub_kind` NULL → `'BT_' || sub_kind` is NULL, nothing matched, **no error** → **walk back** to a function with **two overloads**.
- **Rule out "just late"**: **control group** and **age buckets**, 0% at every age.
- **Result**: **four test gaps** in the postmortem; **one function**, old signature dropped in a **versioned migration**; new **end-to-end test**; rule: an unmappable input must **fail loudly**.
- **Follow-ups**:
  - **Why no exception?** SQL **NULL propagation**: `NULL || x` is NULL.
  - **Why fix forward, not backfill?** Downstream already consumed the wrong state; you need a **correcting entry**. I did not backfill myself.
  - **Fail loudly without killing the batch?** Record rejects to an **error log**.
  - **Which part was yours?** The **root cause and hardening**; the **stopgap** was a teammate's.

### Q18 · How do you build stability and troubleshoot · S1 / S3 / S8 · 60 秒
- **Detect before customers**: **health checks** that say "data is missing", not only "machine is down".
- **Three layers**: **row**, **batch**, **reconciliation**; a mismatch **halts** and **pages**.
- **Fix the class**: after the one fix, **scan the repo** for the next (S8: **42 of 79** similar resources lacked the parameter; **two** real ones flagged, not fixed by me).
- **Fail loudly**: unmappable input is an **error**, never silently dropped.
- **Follow-ups**:
  - **How did you scan?** 【待补：方法（grep / 脚本 / state）】
  - **Narrow your claim?** I once said it was the only such resource; the scan **proved it false**; I now say only what I checked.

### Q19 · SLA and latency metrics you set up and validated · S2 / S1 / S9 · 60 秒
- **S2 handshake**: all enabled checks for a subject area **pass** → status `Completed`; a **07:00 PT** SLA, an alert if a subject area isn't complete.
- **S1**: **reconciliation** against Amex's own summary; **Datadog** alerts on health checks.
- **S9**: **T+7** is an **internal pipeline SLA**; we pay out only after Amex **settles to us**: that separated **expected latency** from a **regression**.
- 【待补：真实的延迟 / 时效数字，如果有】
- **Follow-ups**:
  - **How did you validate the SLA?** 【待补：怎么确认它是对的】
  - **Handshake vs task dependencies?** Consumers are in **different databases or accounts**; a replicated status row is the contract that crosses that boundary.

### Q20 · A cross-team incident · S9 · 60–90 秒
- **Incident**: a large marketplace merchant reported about **$4M** of Amex payouts "missing"; a formal incident channel; I was one of **three fix owners**.
- **My piece 1**: the **SLA** call: **T+7 is internal**, we pay after Amex settles; that separated expected delay from the real **regression**.
- **My piece 2**: the cause was an **effective-date change** for EU compliance that shifted US payouts by a day; I argued for a **region conditional**, not a **revert**.
- **Boundary**: the fix was **deployed by teammates**; "my piece was the **SLA determination and the fix direction**."
- **Follow-ups**:
  - **Why not revert?** A revert breaks the **EU change**; the conditional keeps both correct.
  - **Why did people defer to you?** I was the one who knew the **domain**; take the part you are the authority on.

## D · 协作与成长

### Q21 · A project where communication was difficult · S4 · 60 秒
- **Situation**: a PM's "Australian merchants don't see Amex refund fees" bounced across **3 teams and ~50 replies** before it reached me.
- **Action**: I **pulled the data**, not the org chart: **1,079,627** US refund-fee rows vs **0** in Australia.
- **Root cause**: **config, not code**: every AU merchant's refund policy was `partial`, the logic fires only on `full`; it **predated** our migration.
- **Result**: the thread ended **the same day**, and became a **feature ticket**; I wrote it with a **re-runnable query**.
- **Follow-ups**:
  - **A second issue you weren't sure about?** I said "**not sure yet**" with a layered hypothesis; a senior engineer confirmed it.
  - **How did the PM react?** 【待补：真实反应】

### Q22 · A disagreement with a stakeholder, and what you'd do differently · S3 / S9 · 60 秒
- **S9**: **revert** (fast) vs **region conditional** (robust); I argued for the conditional; the group chose it; I stayed out of the **deploy step**.
- **S3**: ACH on the check's **exclusion list** vs fix the cause; I put **numbers** in writing.
- **Method**: **evidence anyone can re-run**.
- **Gap**: 【待补：一个真实的「我输了然后全力执行」的例子】；没有就说 "My strongest examples are ones where the group agreed; I don't have a clean story where I lost and committed."
- **Follow-ups**:
  - **How do you disagree?** With **evidence anyone can re-run**, not opinion.
  - **Would you do anything differently?** Put the **numbers in the first message**, not the third.

### Q23 · A mistake or failure · S10 / S8 · 60 秒
**Hook：「I'd rather retract my own number in public than have a remediation sized off a bad predicate.」**
- **S10**: my first blast-radius query said **~196K rows, 61 merchants, ~$11K**; **before anyone acted** I re-read the predicate: it never checked the new schedule **existed when the fee was created**; the real scope was **21,923 rows, 30 merchants, $5,854.52**.
- **Root cause**: the refund-fee path **copied the credit's old schedule id** instead of resolving it **at fee time**.
- **S8**: I had said the resource was the **only** one; the scan showed **42 of 79**; I **narrowed my claim**.
- **Rule**: every number ships with a **re-runnable query**; say **when** each input is read.
- **Follow-ups**:
  - **What triggered the re-read?** 【待补：是什么让你重审了谓词】
  - **9× for dollars too?** No: rows ~**9×**, merchants ~**2×**, dollars ~**1.9×**.
  - **Has the fix shipped?** 【待补：是否已合入；确认前不要说「已上线」】

### Q24 · Ambiguity or an inherited project · S6 · 60 秒
- **State on paper**: it only ran in **QA**; I wrote a **State / Handoff / Prod-Cutover** assessment to get the state out of people's heads.
- **Protect what can't be rebuilt**: the **analyst labels** first (exported).
- **Gate the risky part**: phase it behind a **go/no-go**; I'd rather **stop** than ship something that **pages at 3 a.m.**
- **Follow-ups**:
  - **What if the manager wanted it live?** Show the **per-row cost × peak rows** arithmetic and offer the **phased** plan.
  - **Alert volume?** A 99.5% threshold on hundreds of millions of rows a day gives **millions of alerts**; precision was **unknown**.

### Q25 · Prioritization, and speed vs safety · S5 / S8 · 45 秒
- **Reversible → move fast**: a toggle **off by default**; a one-line fix in **7 minutes**.
- **Money paths → shadow-compare first**.
- **Name the exposure** (the one-month dedup window) and write it **next to the code**.
- **Follow-ups**:
  - **What do you do when everything is urgent?** 【待补：你的真实排序方法和一个例子】
  - **What is safe to do quickly?** A **small, re-runnable** change.

### Q26 · Critical feedback and how you handled it · S2 · 60 秒
- **Feedback** (self-review): my quality gate was **table-level**, so a few failing merchants could **block thousands**.
- **First reaction**: I wanted to defend it; I **reviewed it as someone else's code** and wouldn't approve it.
- **Action**: an **ADR** with **four alternatives** and a **"strictest wins"** safety argument. It's **proposed**, not shipped.
- 说「about fifty merchants out of thirty-five thousand」，不说百分比。
- **Follow-ups**:
  - **Did it ship?** No: **proposed**, framework-wide rollout sequenced behind another program.
  - **Feedback from a person?** 【待补：一次真实的、别人给你的批评和你的改变】

### Q27 · Promotion, or your biggest impact · S1 / S5 · 45 秒
- **Impact**: S1 is the **reference** the team points to for onboarding a **file-based settlement source**; S5's backfill SQL became the team's **CDC backfill template**.
- **Promotion**: 【待补：晋升 / 评级的真实情况；没有就只讲影响】
- **Follow-ups**:
  - **How was impact measured?** **Reconciliation** passing, **parity** at cutover; no dollar claim beyond what's documented.
  - **What did you do beyond your ticket?** S7 and the S8 repo scan.

### Q28 · How do you use AI tools; how do you trust AI-written code? · S7 · 45 秒
- **Plan → TDD each phase → gates**: I watch **gates and thresholds**, not lines of code.
- **Money code**: I **read every diff**, including the AI's.
- **Example**: S7, several **agent sessions** running migrations and tests at once; an **on-call copilot** that drafts replies **I review** before sending.
- **In an AI-allowed coding round**: the grade is **working code and complete tests**; I write the **tests first**.
- **Follow-ups**:
  - **When do you not trust it?** Anywhere a **silent wrong answer** costs money; there I recompute by hand.
  - **How do you verify?** Tests, a **second calculation**, a **control group**.
  - **Do you read what it writes?** In money code, **every diff**.

### Q29 · How do you know a change worked? · S10 / S5 · 60 秒
- **Every number has a query**: anyone can re-run it (S10, S4).
- **Say when state is read**: S10's bug was the **time** at which the schedule was read.
- **Validate with what you ship**: S5 ran the **production query** as `count(*)` before cutover.
- **Control group**: S3 used one to rule out "just late".
- **Follow-ups**:
  - **Experiment pitfalls?** **Wrong read time**, **double counting**, **late data**, **a metric that moves for the wrong reason**.
  - **Have you run an A/B test?** 【待补：真实经验；没有就说没有，讲你怎么校验数字】

### Q30 · How would you monitor and roll out an AI feature? · S6 · 60 秒
- **Gate it**: a **go/no-go** with a measured precision, not a launch date (S6).
- **Shadow mode first**: run it **alongside** the current path, compare, no user impact.
- **Watch**: **alert volume**, **precision against labels**, **drift**, and a **fast off** switch.
- **Follow-ups**:
  - **How do you trace an agent's failing tool call end to end?** A **request id** through every hop, **structured logs**, the **inputs and outputs** of each call.
  - **What if there are no labels?** Shadow mode plus a **human-reviewed sample**; precision stays **unknown** until then (S6).

### Q31 · Mentoring, or leading without authority · M1 · 45 秒
- **True**: a newer engineer's **three pieces** plug into my platform; I defined the **boundaries and contracts first** and reviewed designs by **how the same events are consumed on my side**.
- **Also true**: I wrote the team's **onboarding doc** (2024) and still maintain it.
- "I **read every diff**, including the AI's, in money code."
- 不说「I reviewed his PRs」；不编 1:1。【待补：真实的评审或带教经历】
- **Follow-ups**:
  - **Do you review PRs?** Say only what is true: **contracts and design** review.
  - **How do you give a hard review?** 【待补：一次真实的】

## E · 适配与流程

### Q32 · Can you handle a high-intensity workload? · 30 秒
- **Honest**: I've been the **on-call owner** of a money pipeline; I know what a **3 a.m.** page costs.
- **Sustainable**: I fix the **class** of problem (S8) and add **checks that fire first** (S3), so the load goes **down**.
- **Evening calls with Singapore- and China-based teams**: Global Payment's partner teams sit there, so overlap is a US **evening**; fine in principle. 【待补：你能接受的具体安排，例如每周几晚、到几点】
- **Follow-ups**:
  - **Hours?** Be straight about what you can do; don't promise what you can't.
  - **An example of a crunch?** S9: a formal incident with **three fix owners**.

### Q33 · Do you speak Chinese? · 15 秒
- **Plain answer**: 【待补：如实回答你的普通话水平】
- **If the manager switches**: answer in the same language, with the **technical terms in English**.
- **Follow-ups**:
  - **Can you do the project deep dive in Mandarin?** Practise S1 and S5 once in Mandarin; see [[00_how_it_works]].

### Q34 · Your biggest weakness · 30 秒
- **A true one with a plan**: 【待补：你的真实弱点；建议「no hands-on profiling story yet」，计划是「I'm learning to read query profiles and flame graphs」】
- **Evidence**: 【待补：这周你实际做了什么】
- Not "perfectionist".
- **Follow-ups**:
  - **What are you doing about it?** Give the **concrete step** you took this week.
  - **How does it affect the team?** Say what you **ask for** (pairing, a review) to cover it.

### Q35 · Salary expectations · 15 秒
- **Defer**: "I'd like to understand the **role and level** first; the **posted range** works for me."
- The posted base for this req is **$162,000–$387,600** (San Jose), from entry to senior; that is **base only**. The **level** decides where you land: settle it first.
- Don't name a number or quote third-party data.
- **Follow-ups**:
  - **Pushed for a number?** Still defer: ask for the **structure**: base, bonus, RSU schedule.
  - **Other offers?** Say you are in process; no names.

### Q36 · Timeline, location and work authorization · 15 秒
- **Timeline**: "I'm in process elsewhere" 【待补：真实情况】; "this is a priority"; ask the **next steps**.
- **Location**: San Jose; 【待补：愿意去的办公室、每周到岗天数】
- **Authorization**: 【待补：工作许可的真实状态】事实回答，不绕。
- **Follow-ups**:
  - **Start date?** 【待补：通知期】
  - **Which companies?** **No names**, no bluffing.

### Q37 · Any questions for me? · 3–5 分钟
- Pick **three**; ask by interviewer type from [[06-questions-to-ask]].
- Make it about **him**: "What did your first **three months** look like?"
- Close: "Thank you — **[something he actually said]** confirmed my interest."
- **Follow-ups**:
  - **If he answers briefly?** Follow up on one concrete detail, then close.
  - **If time is short?** Ask the **level and next steps** question.

## F · 支付领域简历拷问

### Q38 · How do you make sure a fee calculation is correct? · S10 / S3 / S1 · 90 秒
**Hook：「A fee is only correct if it was computed with the rule that was in force when the money moved, and someone independent agrees with the total.」**
- **Right rule, right time**: S10, the refund-fee path **copied the credit's old schedule id**; the fix resolves the **effective schedule at fee time**.
- **Fail loudly**: S3, an unmappable `sub_kind` made the fee **silently NULL** for about **200 merchants**; now an unmappable input is an **error**.
- **Independent anchor**: S1, fee totals reconcile against the **summary record Amex itself sends**; a mismatch **halts** and **pages**.
- **Integer minor units**, one rounding rule, round **once per line**.
- **Follow-ups**:
  - **A pricing change is back-dated. What happens to fees already computed?** Don't edit them: compute with the new version and write **adjustment lines** for the difference.
  - **How do you test fee logic?** Table-driven cases per rule, plus a **parity run** against production data before release (S5).
  - **Where does rounding happen?** At the **line** boundary, half-even, never in intermediate steps. 【待补：PayPal 费用线上的真实取整规则】
  - **Who owns the pricing configuration?** 【待补：配置的归属和变更流程】

### Q39 · Your settlement job runs twice on the same file. What happens? · S1 / S5 · 60 秒
- **Layer 1**: **file load history**: `COPY INTO` skips a file it has already loaded.
- **Layer 2**: every stage is a **`MERGE` on a business key** (S1 reference number + reject indicator; S5 prefix + invoice number), so a re-run is a **no-op**.
- **Layer 3**: rejects go to an **error log**, keyed the same way, so they don't duplicate either.
- **Say it straight**: "Not exactly-once; **at-least-once plus idempotent writes** is effectively once."
- **Follow-ups**:
  - **What if the same transaction arrives in two different files?** The `MERGE` key is the transaction, not the file; the second is a no-op. 【待补：是否真的遇到过】
  - **What if the job crashes halfway?** Each stage commits in its own **transaction**; the next run picks up from the stream offset and the keys absorb the overlap.
  - **Where can idempotency still break?** S5: a record reprocessed **after the one-month window** bypasses dedup; it's **documented beside the clause**.

### Q40 · Tell me about a reconciliation break you investigated · S1 / S5 / S3 · 90 秒
- **Detection is designed in**: S1 reconciles fee totals against Amex's **own summary record**; S3's daily check said **settled transactions had no fee**.
- **Method**: **slice** the mismatch until one row explains it (S3: one payment type → one row with `sub_kind` NULL); use a **control group** and **age buckets** to rule out "just late".
- **Classify**: timing (S5's **0.07%** were all one-sided same-day records) vs a real conflict (S5: two field differences, both explained).
- **Fix**: correct forward with **new entries**; add the test that would have caught it.
- **Follow-ups**:
  - **Timing difference or real break: how do you tell?** Re-run after the **settlement window**; a timing difference clears itself, a break doesn't.
  - **Who gets told, and when?** 【待补：PayPal 对账差异的升级路径和时限】
  - **How would you reconcile ten million orders a day?** Partition both sides by key, sort, **stream-compare** with two pointers; classify into missing-ours, missing-theirs, amount mismatch.

### Q41 · Walk me through an on-call incident end to end · S3 / S9 · 2 分钟
- **Detect**: S3, a daily check **I built** said settled transactions had **no fee**; S9, a merchant reported about **$4M** of Amex payouts "missing".
- **Triage first**: S9, separate **expected latency** (T+7 is our internal SLA, and we pay only after Amex settles to us) from the **regression**.
- **Root cause**: S9, an **effective-date change** for EU compliance shifted US payouts by a day; S3, SQL **NULL propagation** behind an overloaded function.
- **Fix and prevent**: S9, I argued for a **region conditional**, not a revert; S3, **four test gaps** closed, one function, an end-to-end test.
- **Follow-ups**:
  - **What did you do in the first 30 minutes?** Establish **what is expected** vs broken, size the impact with a **query**, then pick the fix. 【待补：S9 第一个小时的真实时间线】
  - **Why not just revert?** A revert breaks the **EU change**; the conditional keeps both correct.
  - **What did you change so it doesn't recur?** A check that says "**data is missing**", not only "machine is down".

### Q42 · A step is retried, or crashes in the middle. Is the money still right? · S1 / S11 / S5 · 60 秒
- **Assume duplicates**: Kafka and file delivery are **at-least-once**, so every writer is **idempotent**: S11 dedup before insert, **unique constraint** as the backstop.
- **Make the effect atomic**: S1's fee task computes and writes in **one transaction**; there is no state where half a fee exists.
- **Make paths exclusive**: S5's old task **skips interchange** when the toggle is on, so two paths can't **double-charge**.
- **Unknown is not failure**: if a downstream call times out, **query** before retrying with a new id.
- **Follow-ups**:
  - **Would you use exactly-once Kafka?** It covers Kafka-to-Kafka; the effect on a database still needs an **idempotent write**.
  - **Poison message?** S11: the converter returns a **null record** instead of killing the task; bad rows are **recorded, never dropped**.
  - **How do you prove there were no duplicates?** A **uniqueness check** on the business key, plus **reconciliation** of totals.

### Q43 · How does money move from a card transaction to the merchant's bank, and where does your system sit? · S1 / S9 · 60 秒
- **Information flow is fast, money is slow**: authorization and capture are real time; **clearing and settlement** come a day or more later.
- **Closed loop**: Amex sends **one settlement file a day**; we can't book until the file **confirms** settlement (**good-funds model**).
- **My place**: parse and validate the file, compute **fees**, feed **payouts**; US Amex payouts follow our internal **T+7** pipeline SLA.
- **Follow-ups**:
  - **Where is the money between capture and payout?** With the network and acquirer; on our books it's a **receivable**.
  - **Why does Amex differ from Visa / Mastercard?** It is **issuer and network** at once; no standard settlement view, its own file.

### Q44 · Have you worked with refunds, chargebacks or multiple currencies? · S4 / S10 / S1 · 60 秒
- **Refunds**: S4, Australian merchants saw **no Amex refund fees**: **1,079,627** US rows vs **0** in AU; the cause was **config** (refund policy `partial`, logic fires only on `full`).
- **Refund fees**: S10, the refund-fee path used the **credit's old schedule**; real scope **21,923 rows, 30 merchants, $5,854.52**.
- **Regions**: S1's **EU extension** needed a **second feature flag** and a **separate fee ledger**.
- **Chargebacks and FX**: 【待补：真实接触过的拒付或多币种工作；没有就说「I know the mechanics, I haven't owned them」，然后讲机制（[[05-payment-domain]] 第 5、6 节）】
- **Follow-ups**:
  - **How do partial refunds affect reconciliation?** Reconcile the **original plus its refunds** as a group; cumulative refunds ≤ captured.
  - **How do you store amounts across currencies?** **Integer minor units with the currency**; JPY has none, some currencies have three.

### Q45 · What is interchange, and why did your cutover matter? · S5 · 60 秒
- **Interchange**: the fee the **acquirer side pays the issuer**, set by the network, varying by **card type, merchant category and region**; plus **scheme fees** and the **acquirer markup**. Passing them through separately is **IC++**.
- **The problem**: pass-through fees came from a **transaction view** that sometimes filled **after the payout cutoff**; a **settlement view** arrives earlier.
- **My track**: move **credit interchange** to the earlier source: **13.7M rows** at **>99.9%** field parity, **+0.224%** row count, **shipped dark**.
- **Follow-ups**:
  - **Why does timing matter for a fee?** A fee missing at the **payout cutoff** means the payout is **wrong or late**.
  - **Blended vs IC++ for the merchant?** Blended is simple to read; IC++ is transparent and tracks the real cost.

### Q46 · If you rebuilt the fee system from scratch, what would you change? · S1 / S10 / S2 · 90 秒
- **Rules as data**: a **config table** and one generic engine instead of per-format code (S1's six parsers repeat one offset table).
- **Effective-dated, append-only versions**: every fee line stores **rule id and version**, so any number can be **recomputed** (S10's lesson).
- **Fees as ledger entries**: corrections are **adjustment entries**, never updates.
- **Readiness as a contract**: fees wait for a **validated** upstream status, as S2's handshake does.
- **Follow-ups**:
  - **What's the cost of rules as data?** **Runtime** errors instead of compile-time; mitigate with **validation on publish** and a **dry-run** against recent traffic.
  - **How would you migrate?** **Shadow-compute** with the new engine, compare line by line, then switch with a **toggle** (S5).

## 不要说的

- "top committer"、"615 commits"；用「about 90 PRs, the two largest changes in the repo are mine」。
- "I own net settlement"；说「I own the **fee side** / the interchange track」。
- "zero regression"、"merchant by merchant"、"two weeks"（切换）。
- "I profiled it"、"N× faster"（没测过）。
- 美元量级、$55B、$450M/月（项目级数字，不是我的产出）。
- "no bugs"（S3 就在这条线的下游）。
- 商户名、同事名、实习生名。
