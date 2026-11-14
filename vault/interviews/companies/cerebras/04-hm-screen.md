# 04 · 经理面打法（45 分钟）

第一轮是和招聘经理（hiring manager）的 45 分钟视频面。这家公司的经理面最常做的是：让你讲过去做过的系统和当时的技术决策，追问几层，再看你的兴趣和团队对不对得上；可能夹一段"你会怎么测 X"。你的任务是把真实的支付工程经历讲成一个发布集成测试工程师的经历：行为一致性测试、跨阶段的端到端测试、质量门、值班排查、每日健康检查，以及个人项目里的测试体系。AI 是你的缺口，要诚实说清：已经懂什么、怎么学。下面按时间顺序给出要说的话。

## 0. 45 分钟时间线

| 分钟 | 环节 | 你的目标 |
|---|---|---|
| 0–3 | 寒暄、他介绍团队 | 记下他说的团队现状，后面反问用 |
| 3–6 | 自我介绍 | 用 2 分钟版；被打断就停 |
| 6–25 | 项目深挖 | 每个故事 60 秒讲完，停，等追问；追问到第三层要说出边界 |
| 25–35 | 岗位相关的技术讨论 | "你会怎么测 X"按层次答；AI 的部分诚实 |
| 35–40 | 为什么 Cerebras / 为什么这个岗位 | 三句话，不背稿 |
| 40–45 | 你的问题 | 挑 3 个，见 [05-questions-to-ask.md](05-questions-to-ask.md) |

- 每个回答先说结论，再说过程。
- 动作用 "I"，团队的部分明确划线（"the stopgap was a teammate's"）。
- 数字只用故事里的数字；不知道就说量级。

---

## 1. 自我介绍

### 1.1 30 秒版

- **Who**: software engineer at **PayPal**, on **Braintree's fee and settlement platform**.
- **What I'm best at**: proving a change is **safe before it ships**.
- **Three proofs**: Ruby/Kotlin → Java migration behind **behavioral-parity tests**; a **config-driven quality-gate** framework; as **on-call owner**, my own **daily health check** caught a fee bug that **threw no error**.
- **Why here**: I want that to be **the job**, on a stack much **deeper** than mine.

<details><summary>逐字稿（约 85 词，30 秒）</summary>

> I'm a software engineer at PayPal, on Braintree's fee and settlement platform. What I'm best at is proving a change is safe before it ships. I migrated legacy Ruby and Kotlin business logic to Java behind behavioral-parity tests, I built a config-driven quality-gate framework that decides when data is safe to read, and as the on-call owner, a daily health check I built caught a fee bug that threw no error. I want that to be my whole job, on a stack much deeper than mine — which is why release integration at Cerebras.

</details>

### 1.2 2 分钟版

- **Who**: almost **two years** full time at PayPal after an **internship** on the same team.
- **Built**: the **Amex settlement pipeline** end to end; rule: **bad data is recorded, never dropped**; idempotent at three layers.
- **Testing and release work**, four pieces:
  - **Parity**: migrated Ruby/Kotlin logic to Java; same inputs through old and new, **compare outputs**.
  - **Cutover**: **13.7M rows** moved to a new source at **>99.9%** field-level parity; validated with the **production query itself**; **deploy separate from release**, toggle **off by default**.
  - **Quality gates**: one **config-driven** framework; a data set is readable only when **every check passes**; **eight** subject areas on it.
  - **On-call**: tracing and observability (**Sentry**, **Datadog**); a daily health check caught **silent missing fees**; I wrote the postmortem on **why tests missed it** and added an **end-to-end test across pipeline stages**.
- **Outside work**: a Python research platform, **66K lines**, **470+ test files**, **self-hosted CI**; PyTorch training on an **8-GPU** server.
- **Honest line**: I'm **new to ML internals**; I bring the **verification habits** and I'm learning the stack in order.
- **Close**: RIT is the **bridge** between feature and release qualification — the kind of work I've been doing in payments.

<details><summary>逐字稿（约 270 词，2 分钟）</summary>

> I'm a software engineer at PayPal, almost two years full time after an internship on the same team. I own a big part of Braintree's fee platform. I built the American Express settlement pipeline end to end, and its rule is that bad data is recorded, never dropped — every stage is idempotent, and a mismatch halts the pipeline and pages on-call, which is me.
>
> Most of my best work has been on the verification side. When we migrated legacy Ruby and Kotlin logic to Java, I made behavioral parity the bar: the same inputs through the old and the new code, outputs compared. When I moved the interchange-fee track to a new data source, I compared 13.7 million rows field by field — more than 99.9% matched and every difference was explained — then ran the production query itself before cutting over, with the toggle off by default so deploy and release were separate steps. I built a config-driven quality-gate framework: a data set becomes readable downstream only when every check on it passes, and eight subject areas run on it. And as on-call owner, a daily health check I built caught fees that were silently missing; I root-caused it, wrote up the four reasons our tests missed it, and added an end-to-end test across the pipeline stages.
>
> Outside work I built a research platform in Python — about 66 thousand lines, 470-plus test files, self-hosted CI — and ran PyTorch training on an 8-GPU server.
>
> I'm new to ML internals, and I'm learning the inference stack in order. What I bring is the habit of proving a change is safe across components, and RIT is exactly that job.

</details>

- 被问"which part was yours?"：管线从拓扑开始都是我的；NULL 事故的止血 PR 是同事的，根因、复盘和加固是我的。
- 【待补：迁移的规模（多少条业务逻辑、多少测试用例）和最难的一个行为差异】补上之前，迁移只讲方法，不讲数字。

---

## 2. 三个"为什么"

### 2.1 Why Cerebras（45 秒）

- **The product is speed; the cost is integration**: a large model spans many wafers, so the risk sits **between layers**. That's the testing problem I like.
- **RIT is being built from zero**: I've built a quality gate and a test-environment tool **nobody assigned**; I want to **define the gates**, not just run them.
- **Reliability is the contract**: OpenAI's contract has **SLAs** in it; release quality connects straight to revenue, like a missing fee in payments.
- **I use it**: I work with **AI coding agents** every day; faster tokens change how agents work. （只在你确实这样用时说）

### 2.2 Why SDET / release integration（30 秒）

- My strongest work has been **verification**: parity tests, quality gates, health checks, root-cause analysis.
- Here it's **the job, not the 20%** around feature work.
- The posting says "**software engineering applied to quality** … not just execute test cases": I'll be **writing frameworks and tools**, in Python.
- 别说"SDET is easier"或"I couldn't get a SWE role"。

### 2.3 Why leave PayPal（20 秒）

- **Forward-looking**: a deeper stack (compiler → runtime → hardware), a team being **built from zero**, and testing as **the main job**.
- **Credit PayPal**: I own a money pipeline end to end there and learned on-call and root-causing.
- 【待补：真实原因，一句话】如果真实原因是别的（签证、团队变化），说真话，简短，再转回"what I want next"。
- 不批评人和流程；薪资不是理由。

---

## 3. 项目深挖：对着 JD 讲

每个故事：先一句 hook，60 秒讲 S / T / A / R，停，等追问。完整版在 Headlands 的故事页（链接在每节末）。

### D1 · 迁移的行为一致性测试

- **证明 JD 的**："regression validation"、"maintainable, production-quality code"、"end-to-end validation"。
- **Hook**: "When we moved business logic from Ruby and Kotlin to Java, the bar was: the new code does exactly what the old did."
- **Beats**:
  1. **Same inputs, two implementations**: run old and new on the same inputs and compare outputs.
  2. **Classify every diff**: a bug in the new code, a bug in the old code we chose to keep or fix, or an intended change.
  3. **AI-assisted, human-gated**: Claude Code for test generation and refactoring; I read every diff in money code.
  4. 【待补：规模、最难的一个差异、怎么发现的】
- **Follow-ups**:
  - **How do you compare values?** **NULL-aware** equality (`EQUAL_NULL`), because `NULL = NULL` is not true in SQL; that's what I used in the 13.7M-row cutover comparison. 【待补：迁移里数值怎么比】
  - **How did you choose inputs?** 【待补：真实做法：生产样本、边界用例、历史 bug】
  - **How does this map here?** A new compiler or runtime build against a **reference output** is the same idea, with a **tolerance** for floating point.

### D2 · 没有报错的 bug（每日健康检查 + 跨阶段端到端测试）

- **证明 JD 的**："investigate and debug complex cross-stack failures, perform root cause analysis … implement automated tests to prevent regressions"。
- **Hook**: "My hardest bug threw no error: rows that should exist were simply missing."
- **Beats**:
  1. A **daily check I built** found settled transactions with **no fee**, about **200 merchants**.
  2. **Slice → one row → walk back**: `sub_kind` was NULL; `'BT_' || NULL` is NULL; nothing matched, no error; the final `MERGE` called the **wrong overload**.
  3. Ruled out "just late" with a **control group** and **age buckets**; refused to add the type to the check's **exclusion list**.
  4. Postmortem: **four reasons tests missed it**; one function instead of two; old signature dropped in a versioned migration; a new **end-to-end test** across promote → fee.
- **Follow-ups**:
  - **The four gaps?** Tests asserted **routing, not the fee**; the fixture was a **card payload**; pending rows never asserted the field; nothing spanned **promote → fee**.
  - **Lesson for RIT?** Unit tests per stage all passed; the bug lived **between stages**. That is the integration layer.
  - **Who fixed it?** A teammate's **stopgap** landed first; root cause, postmortem and hardening were mine.
- 全文：[S3](../headlands/behavioral/stories/S3_silent-null-root-cause.md)

### D3 · 配置驱动的质量门

- **证明 JD 的**："release qualification pipelines"、"entry and exit criteria"、"actionable quality metrics"。
- **Hook**: "I turned 'is this data safe to read' from a Slack convention into a join condition."
- **Beats**:
  1. Every reconciliation table had its **own hand-written check**; I replaced them with one **config table + generic executor**.
  2. Adding a check = **insert a row**, no deploy; a crashing check becomes a **FAIL record**, not an outage.
  3. When every enabled check passes, a **status flips to Completed**; downstream readers **join on it**.
  4. Rolled out to **eight subject areas**; later I found my own **granularity flaw** — about fifty bad merchants out of thirty-five thousand could block everyone — and wrote an **ADR** for merchant-level readiness ("strictest wins"). It is **proposed, not shipped**.
- **Follow-ups**:
  - **How is that a release gate?** Entry criteria are **checks**, the exit is a **status**, and the consumer **cannot read** until it flips.
  - **Dynamic SQL risk?** Lose **static checking**; the config is engineer-controlled through migrations, so injection isn't the threat.
  - **Did merchant-level ship?** No, **proposed**. 别说上线了。
- 全文：`core/stories/S2 Quality-check 框架.md`

### D4 · 用生产查询本身验证的切换

- **证明 JD 的**："evidence-based recommendations for release qualification"、"risk-based testing"。
- **Hook**: "I validated with the production query itself, so there was no gap between what I tested and what I shipped."
- **Beats**:
  1. Moved credit interchange fees to an **earlier data source**; chose a **static split by fee type** over a smarter fallback (sticky state).
  2. **Field-by-field** full outer join: **>99.9%**; every difference explained (one-sided same-day records).
  3. Ran the **production query** as a `count(*)` on a full day: **+0.224%**.
  4. **Idempotent MERGE**, **toggle off by default**; pre-prod, then production: **13.7M rows** cut over.
- **Follow-ups**:
  - **Why not dual-write?** Two tasks gated in **opposite directions** by one toggle; without that you **double-charge**.
  - **Known risk?** A one-month dedup window: reprocessing **after a month** bypasses dedup; I **documented** it next to the clause.
- 全文：[S5](../headlands/behavioral/stories/S5_cutover-with-the-production-query.md)

### D5 · 确定性的测试环境（schema pool）

- **证明 JD 的**："test infrastructure"、"tooling for test automation"、"engineering efficiency"。
- **Hook**: "Two engineers, or two AI agents, collided on shared-schema DDL, so I built a pool of two-second zero-copy clones."
- **Beats**:
  1. Integration tests ran migrations against **one shared schema**; concurrent runs **collided**.
  2. V1 cloned the shared schema; its state depended on **who migrated last**: not reproducible.
  3. V2 syncs a `MAIN` to the **production-deployed commit**; every slot is a **zero-copy clone**, about **2 seconds**.
  4. **Personal repo**, three ADRs; several agent sessions run migrations and tests **concurrently**.
- **Follow-ups**:
  - **Why 2 seconds?** A clone copies **metadata**, not data; files are **immutable**.
  - **Lesson?** Test state must be **deterministic**: derived from what's deployed, never from who ran last. That's also how you kill a class of **flaky tests**.
- 全文：[S7](../headlands/behavioral/stories/S7_schema-pool-and-why-a-clone-is-fast.md)

### D6 · 个人项目的测试体系（Quant-Stroller）

- **证明 JD 的**："scalable test frameworks"、"CI/CD"、"Python … production-quality code"。
- **Hook**: "I built a research platform to see how much of a good-looking backtest survives realistic costs — and it only works because the tests stop a change from silently moving a result."
- **Beats**:
  1. Python, **66K+ lines**, **470+ test files**, **self-hosted CI**.
  2. **Four narrow interfaces** (data source, factor, strategy, broker): a new market is a thin adapter, so tests stay **at the seam**.
  3. **Two gates** before any strategy is trusted; **340+ experiments** in an **append-only ledger**.
  4. PyTorch training on an **8-GPU** server.
- **Follow-ups**:
  - **What does CI run?** 【待补：每次提交跑什么、多久、有没有分层】
  - **A test that saved you?** 【待补：一个真实例子】
  - **Personal project?** Yes — say it first.
- 全文：[R1](../headlands/behavioral/stories/R1_quant-stroller-research-platform.md)

### D7 · 值班与跨组件排查

- **证明 JD 的**："debugging and observability tools"、"failure analysis"、"shorter debugging cycles"。
- **Hook**: "I'd rather own 'here's the next one' than just the one that paged."
- **Beats**:
  1. **Observability**: transaction tracing with **Sentry** and **Datadog**, so a fee can be followed across stages.
  2. **Terraform release failure in QA**: root cause in **7 minutes** — a missing `outbound_privileges`; same-day deploy to three environments.
  3. Then I **scanned the repo**: **42 of 79** similar resources lacked it; **two** real risks in another module, flagged to the owner.
  4. Rule: **fixing one** and **eliminating the class** are different jobs.
- **Follow-ups**:
  - **How do you start on an unfamiliar failure?** Timeline, then **slice**, then **one concrete case**, then walk back stage by stage.
  - **Why not fix the other module?** Not mine; **flag with evidence**, let the owner decide.
- 全文：[S8](../headlands/behavioral/stories/S8_fix-one-then-scan-the-repo.md)

---

## 4. "你会怎么测 X"

先说一句"Let me clarify what changed and what the risk is"，再按层答。每层一两句，等他挑一层深挖。

### 4.1 测一个推理端点（例如上线一个新模型到 chat completions 接口）

白话先懂这几个词：

| 词 | 白话 |
|---|---|
| **chat completions** | OpenAI 风格的对话接口：发一组消息，返回模型的回答 |
| **流式输出（streaming, SSE）** | 回答一边生成一边一小段一小段地推给客户端 |
| **温度（temperature）** | 控制随机性；设成 0 时每步都选概率最高的 token（**贪心解码**，greedy），结果最可复现 |
| **logits** | 模型对"下一个 token 是哪个"给每个候选打的原始分数 |
| **参考实现（reference）** | 同一个模型在另一套公认正确的环境（比如 GPU 上的 PyTorch）里的输出 |
| **评测集（eval）** | 一组有标准答案的题，用来量准确率 |

- **Clarify**: what changed — a new model, a new runtime or compiler build, a new hardware config? What's the baseline?
- **Contract**: request and response schema; streaming chunks arrive **in order** and **end cleanly**; `stop`, `max_tokens`, **usage counts**; errors (bad input, rate limit); tool calls and **JSON-schema** outputs are valid.
- **Correctness**:
  - **Greedy decoding** against a **reference** run: the first N tokens match, or logits are within a **tolerance**.
  - An **eval suite** score within a threshold of the reference.
  - Exact match isn't always expected, because floating-point **addition order** changes results; so compare **statistically**, not byte for byte.
- **Performance**: **time to first token**, time **between tokens**, **tokens per second per user**, throughput at several **concurrency** levels; compare to the last release with a **noise threshold**.
- **Robustness**: context near the **limit**, empty and Unicode input, **cancel mid-stream**, client disconnect, many requests at once, a node **failing** mid-request.
- **Gating**: what runs per commit, nightly, per release; the **go/no-go** numbers; then a **staged rollout** with monitoring.
- **My link**: "It's the parity testing I did for the Java migration, with a tolerance instead of exact equality."

### 4.2 测一次发布（发布候选的验证）

- **Entry**: the release candidate is cut; each feature's **own qualification** is done; the **known-issue** list is written.
- **Risk map**: diff against the last release — compiler, runtime, kernels, firmware, models. **New interactions** get new scenarios; unchanged areas get the standing regression.
- **Evidence**: unit, simulation, benchmark, feature and integration results **in one view**; gaps **named**, not hidden.
- **Matrix by risk**: models × sizes × context lengths × batch sizes, weighted by **what customers run**.
- **Triage**: every failure **classified** (real regression, flaky, environment, infrastructure, known); real ones **bisected** to a commit and given an owner.
- **Exit**: no open blockers; performance and accuracy within thresholds of the last release; **upgrade and rollback** tested; a written go/no-go **with explicit gaps**.
- **After rollout**: first-pass triage; every **escaped defect** gets a test **at the right layer**; track escape rate, time to triage, and how often master is green.
- **My link**: "My quality-gate framework works the same way: checks are entry criteria, a status is the exit, and nobody reads until it flips."

### 4.3 被问到一个你不会的层

1. 说你知道的最深一层。
2. 说边界："I know it to here."
3. 说你会怎么查：读什么、测什么、问谁。

---

## 5. 诚实说 AI 的缺口

- **Say it first**: "I'm new to ML. I won't pretend otherwise."
- **What I understand, in my words**:
  - Inference runs a model with **fixed weights**; generation is **one token at a time**.
  - **Decode is memory-bandwidth-bound**: every token reads all the weights, so weights in **on-chip SRAM** is why wafer-scale is fast.
  - The trade-off is **capacity**: big models **pipeline across wafers**, so the risk sits **between layers**.
  - **Floating-point** results depend on **operation order**, so comparisons need **tolerances**.
- **What I've touched**: PyTorch training on my **8-GPU** server; apps on the **OpenAI API**; **AI coding agents** daily, with tests as the guardrail.
- **How I learn**: I taught myself backtest statistics by **building** the platform and **testing each piece**; I wrote the team's **onboarding doc** and still maintain it; for ML I'm going **in order** — basics, inference, serving, numerics — and I'd **pair with feature engineers** in the first month.
- **What transfers**: parity testing → **reference comparison**; quality gates → **readiness gates**; on-call RCA → **cross-stack triage**.
- 别说：任何 ML 项目经验；解释不了下一层的术语。

---

## 6. 可能被问的问题（答题提纲）

| 问题 | 提纲 |
|---|---|
| Tell me about yourself | 1.2 节的 2 分钟版 |
| Walk me through the most complex system you built | Amex 管线：文件 → staging → 六个 append-only stream → 六个 MERGE → 两个校验 → 费用；三层幂等；坏数据进错误日志 |
| A technical decision and its trade-off | D4：静态拆分 vs 更聪明的回退；一个月窗口换来扫描量固定，代价是一个月后的去重盲区 |
| Hardest bug | D2 |
| How do you decide what to test? | 先列变化和风险（概率 × 代价），再决定测在哪一层；先断言输出，不只断言路由 |
| How do you handle flaky tests? | 先量化（重跑的通过率）、隔离到单独的队列、找根因（共享状态、时间、并发、环境）；重试只做诊断，不当修复；D5 是消灭一类 flaky 的例子 |
| How do you know a release is ready? | 4.2 节：准入、风险图、五类证据、分诊、准出、上线后 |
| A time you pushed back on shipping | S6 叫停逐行推理的上线；S3 拒绝把真问题加进排除名单 |
| Working with engineers who own the code | S8 先问再推 PR，把别人模块的风险带证据交给负责人；跨团队那场争论用一条查询结束（1,079,627 vs 0 行） |
| What do you know about Cerebras? | [01-company-brief.md](01-company-brief.md) 第 9 节挑 3 条 |
| How do you use AI tools? | 计划 → 每阶段先写测试 → CI 和阈值把关；钱相关代码每个 diff 都读 |
| How strong is your Python? Go? | Python：个人平台 66K 行、470+ 测试文件；工作里主要是 Java 和 SQL。Go："I haven't written Go in production." 【待补：真实的 Go 经验】 |
| Kubernetes and CI experience? | 实习：Kafka proxy 跑在 Kubernetes 里；个人项目自托管 CI。【待补：PayPal 的 CI/CD 里你实际做过什么】 |
| Mentoring | 团队上手文档（2024 年写，一直维护）；先定边界和契约再评审设计；不编 1:1 |
| First 90 days | 先学：一个请求怎么从云走到晶圆、master 现在多红、失败都落在哪；先加诊断和失败分类，再改流程 |
| Pace and hybrid | Sunnyvale 离你近，每周 3 天没问题；发布窗口加班可以接受，问团队怎么轮值。【待补：你真实能接受的程度】 |
| Salary | "I'd like to understand the role and level first." 不报数字 |

## 7. 背景问题 ↔ 故事

| 问题类型 | 首选故事 | 备选 |
|---|---|---|
| 冲突 / 和上级意见不同 | S9：主张 region conditional 而不是 revert | S3：拒绝排除名单 |
| 在没有结构的情况下学新领域 | R1：为了搞懂回测而自建平台，边做边学统计方法 | 【待补：入职时怎么学会费用和结算领域】 |
| 端到端负责 | S1：Amex 管线从桩代码到 18 个月生产 | S7：没人分配的 schema pool |
| 叫停或推迟发布 | S6：用规模估算叫停逐行推理 | S5：默认关闭、先比对再切换 |
| 失败与漏掉的缺陷 | S10：公开撤回自己算错的数字 | S3：测试为什么没抓到 |

## 8. 别说

- "I have ML experience" / 任何没做过的 ML 项目。
- "I profiled it and it got N× faster"：没有这个故事。
- 商户名、同事名、美元总额。
- "merchant-level readiness shipped"：只是提议。
- 批评 PayPal；一上来谈钱。
- 关于 OpenAI 交付进度或股价的评论。
