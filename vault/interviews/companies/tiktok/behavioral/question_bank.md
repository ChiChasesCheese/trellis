# 行为题和 HM 题库（37 题）

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

## A · 开场与动机

### Q1 · Tell me about yourself（≤ 60 秒）· S1 → S5
**Hook：「I'm a backend engineer on PayPal's Braintree fee platform, and what I'm best at is making money pipelines correct and provable.」**
- **Who**: about **twenty months** full time after an **internship** on the same team; Java, Python, SQL; **Snowflake**, **PostgreSQL**, **Kafka**.
- **Flagship**: I **built** the **Amex settlement pipeline** from a stub, about **22M transactions** in half a year, and I owned the **interchange-fee track** of the net-settlement program: **13.7M rows** cut over at **>99.9%** parity.
- **How I work**: every stage **idempotent**, bad data **recorded, never dropped**, validate with the **production query itself**; I'm the **on-call owner** who root-causes quiet data bugs.
- **Why here**: 【待补：为什么是 TikTok 的增长方向，一句话；建议落在「数字必须可信、系统必须可验证」上】
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

### Q3 · Why TikTok, and why this team? · 45 秒
- **A concrete engineering problem**: growth runs on **numbers you can trust**: experiments, attribution, content pipelines; that is the layer I'm good at.
- **Tie to me**: I **retracted my own number** before anyone acted on it, and I validate changes with the **production query**.
- **Public facts only**: the team builds **growth and content-optimization systems**; AIGC, search and discovery. Claim nothing beyond the posting.
- 【待补：你个人真正的原因，一句话】
- **Follow-ups**:
  - **What do you know about the team?** Only what is public: **growth and content optimization**, **AIGC**, **search and discovery**, Web and Lite platforms.
  - **Why not a bigger payments team?** See Q5.
  - **Which TikTok feature do you use, and what would you change?** 【待补：你自己的真实使用和一个具体观察】

### Q4 · Why are you leaving PayPal? · 30 秒
- **Forward-looking**: a **consumer-scale** product, a **faster loop** from idea to measured result, a new class of problems (experiments, AIGC).
- **Credit the place**: "I owned a **money pipeline end to end** and learned on-call and root-causing there."
- **Never** badmouth people or process; salary is never the reason.
- 【待补：真实原因，一句话；签证、地点、团队变化也说真话，简短，然后转向「what I want next」】
- **Follow-ups**:
  - **What did you like least there?** Say what you **want next**, not what you disliked.
  - **Would you stay for a promotion?** 【待补：真实情况】

### Q5 · Your background is payments; this is growth. Why the switch? · 45 秒
- **Same skills**: **data pipelines**, **idempotency**, **reconciliation**, and above all **proving a number is right**.
- **Evidence**: S10 (**196,274 → 21,923** rows, retracted in public) and S5 (**>99.9%** field parity before cutover).
- **Honest gap**: 【待补：你做过的 A/B 实验、指标定义或漏斗分析；没有就说「I haven't run a product experiment platform; I know the failure modes of the numbers behind one」】
- **Follow-ups**:
  - **What's a failure mode of an experiment metric?** **Reading state at the wrong time** (the S10 lesson), **double counting**, **late-arriving data**.
  - **What would you learn first?** The team's **metric definitions** and how an experiment's result is **computed and audited**.

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
- **Evening calls with China-based teams**: fine in principle. 【待补：你能接受的具体安排】
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
- The posted base for this Senior role is **$218,400–$387,600**; that is **base only**.
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

## 不要说的

- "top committer"、"615 commits"；用「about 90 PRs, the two largest changes in the repo are mine」。
- "I own net settlement"；说「I own the **fee side** / the interchange track」。
- "zero regression"、"merchant by merchant"、"two weeks"（切换）。
- "I profiled it"、"N× faster"（没测过）。
- 美元量级、$55B、$450M/月（项目级数字，不是我的产出）。
- "no bugs"（S3 就在这条线的下游）。
- 商户名、同事名、实习生名。
