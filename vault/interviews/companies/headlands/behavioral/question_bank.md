# 背景问题题库（36 题）

- 每题：故事标签 · 时长 · 三到四条可直接说出口的要点（加粗是路标）· 2–4 个追问和一行回答要点。
- 先讲 L1，停，等追问。
- 【待补：…】 补完前不要口播；每题给了补不出来时的诚实降级。

## A · 开场与动机

### Q1 · Tell me about yourself（≤ 60 秒）· S1 → S3 → R1
**Hook：「I'm a software engineer at PayPal, and what I'm best at is correctness and testing.」**
- **Who**: about **twenty months** full time after an **internship** on the same team; a payments **fee platform**.
- **Flagship**: I **built** the **Amex settlement pipeline** and the **fee calculation**; mostly **Snowflake** and **Postgres**, more **Java** as we migrate Ruby/Kotlin logic behind **parity tests**; I'm the **on-call owner**, root-causing quiet data bugs.
- **Outside work**: a **research and backtesting platform**, to see how much of a backtest **survives realistic costs**.
- **Why here**: the **infrastructure under a research platform**; strong at **correctness and testing**, **building depth below the JVM**, on a **small team** where changes reach production in **weeks**.

<details><summary>逐字稿（147 词 ≈ 59 秒）</summary>

> I'm a software engineer at PayPal, about twenty months full time after an internship on the same team. I work on a payments fee platform: I built the American Express settlement pipeline and the fee calculation on top of it, mostly Snowflake and Postgres, with more and more Java as we migrate older Ruby and Kotlin logic behind parity tests. I'm also the on-call owner, so I spend my time root-causing quiet data bugs and writing the tests that would have caught them. Outside work I built a research and backtesting platform, because I wanted to know how much of a good-looking backtest survives realistic costs. That's why this role appeals: it's the infrastructure under a research platform. My strength is correctness and testing; I'm deliberately building depth below the JVM, and I'd like to do that on a small team where changes reach production in weeks.

</details>

- "depth below the JVM" 只有你确实在做时才说。
- 被打断问 Java 迁移：【待补：迁移里最难的一个行为差异】。
- **Follow-ups**:
  - **Which part was yours?** Everything from the **topology** of the Amex pipeline onward; in the S3 incident the **stopgap** was a teammate's.
  - **Why correctness and testing?** My tests once asserted **routing, not the fee**; now I assert on the **output** and add checks that fire on **missing data**.

### Q2 · Walk me through your resume · S1 · 3 分钟
- **PayPal full time**: Amex pipeline (**~22M transactions** in half a year) → **net-settlement fee track** (**13.7M rows** cut over at **>99.9%** parity) → **on-call** and observability (Sentry, Datadog).
- **Internship**: Kotlin/Spring service, **Kafka** consumers into the warehouse, **Spark + Airflow** validators.
- **NYU MS CS** after a **construction-management BS**: "I switched into CS for my master's and have been writing production code since."
- **After each block, stop**: "I can go into the pipeline or the cutover."
- **Follow-ups**:
  - **Go deeper on the pipeline.** Stop after L1; offer S1 or the cutover (S5) and wait.
  - **What did the internship teach?** Kafka sink: parallelism = **replicas × tasks.max**, **capped by partition count**.
  - **Why the switch into CS?** "I switched into CS for my master's and have been writing production code since."

### Q3 · Why trading? · R1 · 45 s
- **Curiosity**: I built a backtester to find out **how much of a good-looking backtest survives costs**; it taught me to **distrust my own results**.
- **What I like**: results are **measured** and unforgiving. 【待补：你个人真正的原因，一句话】
- **Honest limit**: "I'm not a trader; what I'm good at is the **infrastructure and correctness** under it."
- 降级：只讲第一条和第三条；别发挥金融知识。
- **Follow-ups**:
  - **What did the backtester teach you?** To **distrust my own results**: most ideas **die at the gates**, and the **ledger** shows how many.
  - **Do you trade yourself?** 【待补：你个人是否交易、一句话怎么说】 The project side: **paper trading only**, and it is **not proof of profit**.

### Q4 · Why Headlands? · R1 · 30 s
- **Three reasons**: changes reach production in **weeks**, not quarters; the Java role is the **research-platform infrastructure** (storage, compute, monitoring); you hire for **curiosity** and teach the finance.
- **Tie to me**: my backtester made me care about the layer **under the research**.
- "I'd rather be hired for **how I debug** than for what I've memorized."
- 不加没读过的东西。
- **Follow-ups**:
  - **What do you know about us?** Only what is **public**; claim nothing beyond it.
  - **What do you want to learn here?** The **machine layer** (caches, syscalls, networking, the JVM) on real production systems.

### Q5 · Why the Java role rather than C++ or research? · 30 s
- My **production strength is Java and SQL**, and this role is **platform, storage, monitoring**.
- The **hot path is C++**; I want to **earn** depth there, not claim it.
- I'm **open on language**: the interviewer may choose C++, and I'm preparing both.
- **Follow-ups**:
  - **So are you a C++ person?** Open on language: the **hot path is C++**, I want to **earn** that depth, not claim it.
  - **Why not research?** My strength is **correctness, testing, platform and storage**.

### Q6 · Why are you leaving PayPal? · 30 s
- **Forward-looking**: a **smaller team**, a **shorter loop to production**, the layer **below the JVM**. 【待补：真实原因，一句话】
- **Credit the place**: "I own a **money pipeline end to end** there and learned on-call and root-causing."
- **Never** badmouth people or process; salary is never the reason.
- 如果真实原因是别的（签证、地点、团队变化），说真话，简短，然后转向"what I want next"。
- **Follow-ups**:
  - **What did you learn there?** Owning a **money pipeline end to end**, on-call, and root-causing quiet data bugs.
  - **Anything you disliked?** Do not criticise people or process; say what you **want next**.

### Q7 · Where do you want to be in 2–3 years? / What do you want to learn? · 30 s
- **Learn the machine layer**: **caches, syscalls, networking, the JVM**, on real production systems.
- **Own a piece** of the platform and **propose a change** I can defend with numbers.
- **Year one is closing the gap**: I expect it to take time to get fully up to speed.
- **Follow-ups**:
  - **What would you do in year one?** **Close the gap**: learn the machine layer and expect it to take time.
  - **What would you own?** A piece of the platform, and **propose a change defended with numbers**.

## B · 语言与"各层都懂"

### Q8 · Java vs C++: when would you choose which? · 60 s
- **C++**: **deterministic memory and layout**, no GC pauses, control over **cache behavior**, which matters on the **hot path**.
- **Java**: **productivity**, safe memory, ecosystem, and a **JIT** that gets close to C++ on steady-state code; costs are **GC**, **warm-up**, **object layout**.
- **Choose by the bottleneck**: **platform and tooling → Java**; **microsecond-sensitive path → C++**.
- 被追问 GC/JIT/逃逸分析：说到你会的那层，"below that I'd measure or read the docs."
- **Follow-ups**:
  - **What does the JIT cost you?** **Warm-up**, plus **GC** and **object layout** effects.
  - **What if GC pauses matter?** Say the deepest layer you know, then "below that I'd **measure** or read the docs."

### Q9 · How much C++ have you written? · 15 s
> "My C++ is **【待补：真实的量，课程 / 刷题 / 项目，一句话】**. I haven't shipped production C++; my production languages are **Java and SQL**. I know the model — **RAII, move semantics, smart pointers** — and I've been writing practice problems in **C++20 with sanitizers**. I'd expect to be slower than your team for a while."
- 说**真实的量**；**不夸大**；说出**学习计划**。
- "practice problems in C++20" 只有真的做了才说。
- 被追问某个特性：会就答，不会 "I know it to X; below that I'd check the reference."
- **Follow-ups**:
  - **Can you explain RAII?** I know the model: **RAII, move semantics, smart pointers**; answer what you know, stop at the edge.
  - **How long to be productive?** "I'd expect to be **slower than your team for a while**", with the learning plan.

### Q10 · How well do you know Linux and networking? · 30 s
- **User level**: I know it as a **user of Kafka, gRPC, Snowflake**, not as a **tuner**. 【待补：任何真实的 Linux/网络经验——自托管服务、CI 机器、排查网络问题】
- **What I understand**: **latency vs throughput** via **batching**, **Nagle's algorithm**, **serialization cost**.
- **How I'd start**: "I'd **measure where the time goes** first" — then ask what the current bottleneck is.
- **Follow-ups**:
  - **What is Nagle's algorithm?** It **batches small writes** to cut packets, at the cost of **latency**.
  - **How would you find a network bottleneck?** **Measure where the time goes** first, then ask what theirs is.

### Q11 · Have you worked on distributed storage or a compute farm? · 45 s
- **Consumer side of a scaled system**: Kafka sink into the warehouse, **one deployment per topic**, parallelism = **replicas × tasks.max**, **capped by partition count**.
- **Storage model as a user**: **immutable micro-partitions + metadata** (why clones are cheap and pruning works); **append-only streams with offsets**.
- **Boundary**: "I **haven't operated** a cluster or **designed** a storage engine; I **understand the model** and I'd learn yours."
- **Follow-ups**:
  - **How does Kafka sink parallelism work?** **Replicas × tasks.max**, **capped by partition count**.
  - **Why are clones and pruning cheap?** **Immutable micro-partitions + metadata** pointers.
  - **Have you operated a cluster?** No; I **understand the model** and would learn yours.

### Q12 · How strong are you in Java, really? · 30 s
- **Daily**: Java and Snowflake at PayPal; Kotlin/Spring on the internship; the **Java coding test passed**.
- **Migration**: Ruby/Kotlin → Java with **parity tests**. 【待补：规模与最难的行为差异】
- "**Fluent**, not a JVM-internals expert; I know **JIT and GC at the level of when they matter**, and I'm drilling Java 21."
- 不说 "superior"。
- **Follow-ups**:
  - **How do you know the Java rewrite is right?** **Parity tests**: same inputs, compare outputs old vs new.
  - **JIT and GC?** Known "at the level of **when they matter**"; I am drilling Java 21.

## C · 技术经历

### Q13 · Tell me about a performance problem you solved · S6（诚实版）· 60–90 s
- **Say the boundary first**: "The honest version is **capacity reasoning before shipping, not profiling a running system**."
- **S6**: a detector that only ran on **6 synthetic merchants**; production ~**18,000 merchants**, up to **760M rows** a day; **per-row cost × peak rows** → timeout; Phase 1 as **set-based SQL**, model **behind a gate**.
- **S5**: a **one-month window** on the merge's `ON` keeps the scan **bounded** (zone-map pruning); the cost is a **dedup blind spot after a month**.
- **Method**: "If it were live I'd **measure per-row latency at small N**, separate **CPU from data movement**, extrapolate." Then ask what their bottleneck is. 永远不编"快了 N 倍"。
- **Follow-ups**:
  - **Did you profile it?** **No**; it never ran at scale. I'd measure **per-row latency**, then **CPU vs data transfer**.
  - **Why is per-row numpy slow here?** Per-row **call overhead** and **data movement**; a set-based query does **one scan** in place.
  - **How decide Phase 2 is worth it?** A **business driver** plus **measured precision** in shadow mode.

### Q14 · Hardest bug you've debugged · S3 · 75 s
- **No error, just missing rows**: a **daily check** I built found settled transactions with **no fee**; ~**200 merchants**.
- **Method**: **slice** → **one row** → **walk back**; cause: **NULL concatenation** plus a **function overload** the final `MERGE` picked wrongly.
- **Tests and fix**: **four reasons** tests missed it; **one function**, **versioned DROP**, new **end-to-end test**; rule: **fail loudly**.
- 备选：Terraform 的 7 分钟 RCA（S8）。
- **Follow-ups**:
  - **Why no exception?** **NULL propagation**: `NULL || x` is NULL, the lookup found **no match**, so **no row**.
  - **Why not add ACH to the exclusion list?** It makes a **loud** detector **silent**; the fees were really missing.
  - **Did you backfill?** **Fix forward** with a correcting entry; I did **not** backfill myself.

### Q15 · How do you test? · S3 + S5 + R1 · 60 s
- **Test the output, not just the route**: our tests asserted **routing** but never the **fee**; the **fixture** didn't match the real population.
- **Validate with the thing you ship**: I ran the **production query itself** as a count (**+0.224%**) after a field-by-field comparison (**>99.9%**).
- **Tests protect results**: my backtester has **470+ test files** and **two gates** for strategies.
- "A check that fires on **missing data** beats a dashboard nobody opens."
- **Follow-ups**:
  - **What was wrong with the fixture?** It was a **card payload**; it must look like the **real population**.
  - **Most general lesson?** Assert on the **output**, not only the route.

### Q16 · How do you ship fast and still know it's safe? · S5 · 45 s
- **Deploy ≠ release**: merge with the **toggle off**, enable in **pre-prod**, then production.
- **Reversible**: the toggle is a **fast off**; paths are **mutually exclusive by source filtering**, so nothing double-counts.
- **Compare first**: shadow-compare, **count** on a full day, then cut over.
- **Follow-ups**:
  - **Why not dual-write?** Two tasks **gated in opposite directions** by one toggle are the exclusion; without it you **double-charge**.
  - **What can still go wrong?** Reprocessing **past the window**; the toggle gives a **fast off**.

### Q17 · An incident you handled / your on-call · S3 / S9 · 75 s
- **S3**: my own check caught it; **root cause in minutes**; I owned **RCA and hardening**; the stopgap was a teammate's.
- **S9**: a marketplace merchant's ~**$4M** of payouts looked "missing"; I was **one of three owners**; I settled the **SLA question** (T+7 is our internal SLA; we pay out after the network settles to us) and argued for a **region conditional** over a **revert**; closed in **three days**.
- **Habits**: a mismatch **halts** the pipeline and **pages**. 【待补：值班频率】
- 修复由同事部署；我的是 SLA 定论 + 修法方向。
- **Follow-ups**:
  - **How did you find S3?** The **daily health check I built** flagged settled transactions with no fee.
  - **Who deployed the S9 fix?** A teammate; mine was the **SLA conclusion** and the **fix direction**.

### Q18 · Biggest system you built; walk me through the design · S1 · 2 分钟
- **Flow**: fixed-width file → staging → **six append-only streams** → **six `MERGE`s on a composite key** → **two validators** → fee task.
- **Idempotent at three layers** (load history, merge keys, error log); **bad data goes to an error log**, never dropped.
- **Failures and changes**: **late files** (scan all date partitions); **six copies of the offset table** → one config-driven parser.
- **Follow-ups**:
  - **Why not Airflow or Spark?** **Data locality** and **transactional** steps in the warehouse; cost is **weaker orchestration**, so I built monitoring on top.
  - **Exactly-once?** No; **at-least-once plus idempotent writes** is effectively once.
  - **Two upstream tasks out of step?** `AFTER A, B` guarantees each ran, not the **same batch**; mismatches go to the **error log** and **self-heal** next run.

### Q19 · A design decision you'd change · S1 / S7 · 45 s
- **S1**: the **offset table repeated six times** → a **config table + one generic parser**.
- **S7**: V1 cloned from a **shared schema** whose state depended on **who migrated last**; V2 derives from the **deployed commit**.
- **Pattern**: make the system's **input a single deterministic thing**.
- **Follow-ups**:
  - **Why a config table?** The six parsers **repeat one offset table**.
  - **What broke in V1?** Source state was **history-dependent** (who migrated last).

### Q20 · Something you dug into out of curiosity · S8 / S7 / R1 · 45 s
- **Terraform**: after the fix I **scanned the whole repo**: **42 of 79** resources lacked the parameter; **two** real, same-shape risks.
- **Clones**: I wanted to know **why a clone takes two seconds**: **immutable partitions + metadata**.
- **Backtester**: built to find out what **survives costs**.
- **Follow-ups**:
  - **Why were future grants harmless?** They have **no existing dependents** to conflict with.
  - **Why is a clone 2 seconds?** **Immutable micro-partitions + metadata pointers**; no data copied.

### Q21 · Something you built that nobody asked for · S7 · 60 s
- **No ticket, no owner**: tests shared one schema; two engineers or **two AI sessions** collided on DDL.
- **V1 → V2** rewrite with **three ADRs**; **zero-copy clones in ~2 seconds**; **deterministic** from the deployed commit.
- **Boundary**: **personal repo**; an **on-call copilot** I built on top was adopted by adjacent teams.
- **Follow-ups**:
  - **Cross-database streams?** Clone the **replication DB first**, then **auto-repair** after a swap.
  - **Why direct-push to main?** **Personal repo**; it does not touch team code.

### Q22 · How do you use AI tools; how do you trust AI-written code? · 45 s
- **Plan → TDD each phase → gates**: I watch **gates and thresholds**, not lines of code.
- **Money code**: I **read every diff**, including the AI's.
- "For this interview I'm working **without** it, and I've practiced that way." (只有真的关掉练过才说)
- **Follow-ups**:
  - **Do you read what the AI writes?** In money code I **read every diff**.
  - **What do you watch instead?** **Gates and thresholds**, not lines of code.

## D · 工作方式

### Q23 · A time you disagreed with someone · S9 / S3 · 60 s
- **S9**: **revert** (fast) vs **region conditional** (robust); I argued for the **conditional**; the group chose it; I stayed out of the deploy step.
- **S3**: someone suggested adding ACH to the **exclusion list**; I put the **numbers** in writing; the check stayed.
- **Method**: **evidence anyone can re-run** (a cross-team thread: **1,079,627 vs 0** rows).
- 缺口：没有"我输了然后全力执行"的故事。【待补：一个真实的"我输了然后全力执行"的例子】；没有就说 "My strongest examples are ones where the group agreed; I don't have a clean story where I lost and committed."
- **Follow-ups**:
  - **Why keep the check as is?** Adding ACH to the exclusion list would hide **real missing fees**.
  - **How do you disagree?** With **evidence anyone can re-run**, not opinion.

### Q24 · A mistake or failure · S10 / S8 · 60 s
- **S10**: my first number was **~9× too many rows** (196,274 → 21,923); I found it **before anyone acted** and **retracted it**.
- **S8**: I had said it was the **only** such resource; the scan showed **42 of 79**; I **narrowed the claim**.
- **Mechanism**: every claim now ships with a **re-runnable query**; I **state when** each state is read.
- **Follow-ups**:
  - **What was wrong with the predicate?** No check that the **schedule existed at fee-creation time**.
  - **Root cause in one sentence?** The path **copied the credit's historical schedule id** instead of **resolving at fee time**.

### Q25 · Critical feedback and how you handled it · S2 · 60 s
- **Feedback**: my quality gate was **table-level**, so a few failing merchants could **block thousands**.
- **First reaction**: I wanted to defend it; I **reviewed it as someone else's code** and wouldn't approve it.
- **Action**: an **ADR** with **four alternatives** and a "**strictest wins**" safety argument; it's **proposed**, not shipped.
- 不说百分比，只说 "about fifty merchants out of thirty-five thousand"。
- **Follow-ups**:
  - **What alternatives did the ADR weigh?** **Four alternatives** and a "**strictest wins**" safety argument.
  - **Did it ship?** No: it is **proposed**, not shipped.

### Q26 · Working across teams / with non-engineers · S4 / S9 · 45 s
- **Cross-team thread**: **three teams, 50 replies**; I **pulled the data**: **1,079,627 refund-fee rows vs 0**, root cause a **config value**, and showed it **predated** our migration.
- **Wrote it so others could re-run it**; it ended the thread and became a feature ticket.
- **Said "not sure yet"** on a second fee kind, with a **verification plan**.
- **Follow-ups**:
  - **How did the thread end?** **1,079,627 vs 0** refund-fee rows; the root cause was a **config value** that **predated** our migration.
  - **What if you were unsure?** Say "**not sure yet**" and give a **verification plan**.

### Q27 · Code review / mentoring · M1 · 45 s
- **True**: a **newer engineer's three pieces** plug into my platform; I **defined boundaries and contracts first** and reviewed designs by **how the same events are consumed on my side**.
- **Also true**: I wrote the team's **onboarding doc** in 2024 and still maintain it.
- "I **read every diff**, including the AI's, in money code."
- 不说 "I reviewed his PRs"；不编 1:1。【待补：真实评审经历】
- **Follow-ups**:
  - **Do you review PRs?** Say only what is true: **contracts and architecture** review; **read every diff** in money code.
  - **Any mentoring?** The team's **onboarding doc** (2024), still maintained.

### Q28 · Ambiguity or an inherited project · S6 · 60 s
- **Only ran in QA**; I wrote a **State / Handoff / Prod-Cutover** assessment to get the state out of people's heads.
- **Protect what can't be rebuilt**: the **analyst labels** first.
- **Gate the risky part** (go/no-go); I'd rather **stop** than ship something that pages at **3 a.m.**
- **Follow-ups**:
  - **What did you protect first?** The **analyst labels**, the one irreplaceable piece: **exported first**.
  - **Why stop instead of ship?** A launch that **pages at 3 a.m.** costs more than a gated plan.

### Q29 · Someone knew more than you / being told what to do · S9 / S8 · 45 s
- **S9**: a senior teammate **deferred to me** on one SLA; on the **deploy** I **deferred** and let the others land it.
- **S8**: I **asked before pushing** a PR in a repo where I was only cc'd.
- I like **owning ideas**, and I **ask first** where I'm a guest.
- **Follow-ups**:
  - **When did you defer?** On the S9 **deploy** I let the others land it.
  - **What if the repo isn't yours?** I **asked before pushing** a PR where I was only cc'd.

### Q30 · Speed vs safety · S5 / S8 · 45 s
- **Reversible → move fast** (a toggle **off by default**); **money paths → shadow-compare** first.
- **Small and re-runnable** changes are safe to do quickly (a one-line fix in 7 minutes).
- **Name the exposure** (a one-month dedup window) and write it **next to the code**.
- **Follow-ups**:
  - **What is fast and safe?** A **small, re-runnable** change, e.g. a one-line fix in **7 minutes**.
  - **What about the exposure?** **Name it** (the one-month dedup window) and write it **next to the code**.

## E · 面向未来与流程

### Q31 · What would you look at first if you joined? · 45 s
- **Learn**: how a researcher **submits and reruns** work; where **time and failures** go.
- **Instrument before optimizing**: **measure** the slow path; add a **missing-data check** so the system **tells you first**.
- **Ask**: "What's the **slowest step** for a researcher today?"
- **Follow-ups**:
  - **How would you measure first?** Time per stage and rows per second for a researcher's job, **before optimizing**.
  - **What would you ask them?** "What's the **slowest step** for a researcher today?"

### Q32 · Any questions for me? · 3–5 分钟
- Pick three: **"What are the biggest pieces of the research platform, and which is hardest to keep fast?"**; **"Tell me about a recent performance problem — your code, a library, or the OS?"**; **"What do you look for in a session like this, and what are the next steps?"**
- Make it about him: "What did your first **six months** look like?"
- Close: "Thank you — **[something he actually said]** confirmed my interest."
- **Follow-ups**:
  - **Why these questions?** They show you think about **performance** and about **his** experience.
  - **If he answers briefly?** Follow up on one concrete detail he gave, then close with thanks.

### Q33 · Salary expectations · 15 s
- **Defer**: "I'd like to understand the **role and level** first; the **posted range** works for me."
- The posted base for the Java role in Chicago is **$175k–$300k**; that is **base only**.
- Don't name a number or quote third-party data.
- **Follow-ups**:
  - **Pushed for a number?** Still defer: the **posted range works**, **base only**.
  - **Third-party data?** Do not quote it.

### Q34 · Timeline / other interviews · 15 s
- **Honest and short**: "I'm in process elsewhere." 【待补：真实情况】; "this is a priority."
- No company names, no bluffing.
- Ask: "What are the **next steps** and **timeline**?"
- **Follow-ups**:
  - **Which companies?** **No names**, no bluffing.
  - **What do you ask back?** The **next steps** and **timeline**.

### Q35 · Relocation / location / work authorization · 15 s
- The Java role is open in **Chicago, New York, London, Amsterdam**; you are in **San Jose**.
- 【待补：愿意去哪个办公室；工作许可的真实状态】事实回答，不绕。
- **Follow-ups**:
  - **Which office?** Chicago, New York, London or Amsterdam: answer with facts.
  - **Work authorization?** A plain factual answer; do not hedge.

### Q36 · Biggest weakness / anything to add · 30 s
- **A true one with a plan**: "**Below the JVM** — caches, networking, profiling — and I'm **closing it deliberately**."
- **Evidence**: 【待补：这周你实际做了什么，一句话】
- Not "perfectionist".
- **Follow-ups**:
  - **What are you doing about it?** Give the **concrete step** you took this week.
  - **Why not "perfectionist"?** It is a dodge; a **true weakness with a plan** is credible.
