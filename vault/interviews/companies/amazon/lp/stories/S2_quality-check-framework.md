# S2 · Quality-check 框架 + 商户级 ADR（平台化 / 自我纠错）

> 来源：`core/stories/S2 Quality-check 框架.md`（status: **partial**）。ADR 状态是 **Proposed**。
> 主 LP：**Invent and Simplify · Insist on the Highest Standards · Earn Trust · Frugality**；副：Are Right A Lot · Have Backbone · Think Big · Hire and Develop。
> 一句话：*"I replaced hand-written validation tasks with a config-driven quality gate that downstream teams join on, then wrote the ADR that overturned the granularity of my own design."*

## 1. 数字

| 数字 | 口径 |
|---|---|
| 框架 PR ~1,500 行（#1997，+1489） | 框架本体 |
| 铺开 8 个 subject area，各 200–800 行 | 我自己铺 |
| ~50 个持续失败商户（~4%）挡住 35,000 个商户 | 生产数据，ADR 动机 |
| 96.4% 的检查一次通过 → 只存失败行 | ADR 容量论证 |
| 极端每月 ~80 万行（失败行） vs 每商户每次一行 = 每天 240 万行 | ADR 容量论证 |
| 方案 D 的先例：TRANSFERS 区域已跑 16 个月 | 唯一已证明的 subject area |

**状态口径（必须背）**："The framework and eight rollouts are live; merchant-level readiness is designed, reviewed, and proven for one subject area, and the framework-wide rollout is sequenced behind the net-settlement ramp." **不说**「已改成商户级 / 上线效果」。

## 2. 60–90 秒口述提纲

**I replaced hand-written validation tasks with a config-driven quality gate, then wrote the ADR that overturned the granularity of my own design.**

**S · Situation**
- The team had **dozens of reconciliation tables**, each with its own **hand-written validation task**.

**T · Task**
- Make adding a check cheap, and make "is this data safe to read" a **hard condition**, not a Slack convention.

**A · Action** (in the order it happened)
1. Built a **config table**: one row says which stored procedure runs for which subject area, with what **SLA**.
2. Built a **generic executor** that writes a normalized pass / fail / warning row; an **exception handler** isolates broken checks.
3. Added a status row that flips to **Completed** and replicates to a share layer — downstream teams **JOIN** on it.
4. **Rolled it out** across eight subject areas myself — adding a check became inserting a row.
5. At production scale I saw **my own flaw**: readiness was per table, so ~**50 bad merchants** of **35,000** blocked everybody.
6. Wrote an **ADR** — four alternatives, a correctness argument, a volume analysis.

**R · Result**
- Framework and **eight rollouts live**; merchant-level readiness **designed, reviewed, proven in one subject area**.
- Broader rollout is **sequenced behind net settlement** — not claimed as shipped.

**L · Learning / Mechanism**
- **Granularity** is a design parameter to revisit at scale; I fix my own flaws through a formal **ADR**.

<details><summary>逐字稿（参考，不背）</summary>

> Our team had dozens of reconciliation tables, and every new one got its own hand-written validation task. I replaced that with a config-driven quality-check framework. One row in a config table says which stored procedure to run for which subject area, with what SLA. A generic executor builds the call, captures the result, and writes a normalized pass, fail or warning row, and an exception handler means one broken check never takes down the others. When every enabled check passes, a status row flips to `Completed` and replicates to a share layer where downstream teams `JOIN` on it. So "is this data safe to read" went from a Slack convention to a SQL condition.
>
> I rolled it out across eight subject areas myself — adding a check became inserting a row. Then I saw a flaw in my own design: readiness was per table, so roughly fifty bad merchants out of thirty-five thousand blocked everybody. I didn't patch it quietly. I wrote an ADR: four alternatives, a correctness argument, and a volume analysis. The direction is reviewed and proven in one subject area; the broader rollout is sequenced behind the net-settlement work.

</details>

## 3. 2 分钟口述提纲

**I replaced hand-written validation tasks with a config-driven quality gate, then wrote the ADR that overturned the granularity of my own design.**

**S · Situation**
- Every reconciliation table — acquirer settlement, adjustments, tax, transaction reconciliation — had its **own validation task**.
- Each new table meant **write, review, deploy** another task.

**T · Task**
- I **owned** replacing that with one **platform** other people plug into.

**A · Action** (in the order it happened)
1. Built a **contract-config table**: procedure name, date column, **SLA hours**, JSON parameter blob.
2. Built a generic **executor** with `EXECUTE IMMEDIATE` that writes PASS / FAIL / WARNING; crashes become a **FAIL row**.
3. Built a **trigger-status** state machine: all enabled checks pass, status becomes **Completed**, replicated to a share layer.
4. Accepted the **dynamic SQL** trade-off — no static checking; config is migration-controlled, plus a **health check** on the results table.
5. Shipped the ~**1,500-line** framework, then **rolled out eight subject areas** myself.
6. Saw my **own flaw**: ~50 failing merchants (~4%) blocked **35,000**; wrote an **ADR** with four options.
7. Rejected **VARIANT** (kills pushdown), **flatten** (size cap), a **new table** (new infrastructure); chose **summary row plus per-merchant failure rows**, "**strictest wins**".

**R · Result**
- **96.4%** of checks pass, so only failures are stored: at worst ~**800K rows a month**, not 2.4M a day.
- Framework and **eight rollouts live**; merchant-level **designed, reviewed, proven** in one area (16 months); rollout sequenced behind net settlement.

**L · Learning / Mechanism**
- Downstream **joins on a status row** — safety is a SQL condition, not a convention.
- **What I'd do differently:** ask "who is the **blast radius** if one check fails?" before designing any gate.

<details><summary>逐字稿（参考，不背）</summary>

> **Problem.** Every reconciliation table — acquirer settlement, adjustments, tax, transaction reconciliation — had its own validation task, so each new one meant writing, reviewing and deploying another task.
>
> **What I built.** Three pieces. A contract-config table, one row per subject area and validation: the procedure name, date column, SLA in hours, and a JSON parameter blob. A generic executor that builds the call with `EXECUTE IMMEDIATE`, reads the result back, and writes PASS, FAIL or WARNING — with an exception handler that turns a crash into a FAIL row. And a trigger-status state machine: when every enabled check for a subject area passes, the status becomes `Completed` and is replicated to a share layer. Downstream consumers join on it — the interchange-source migration I did later is one of them. The trade-off I accepted is dynamic SQL: no static checking, so a typo in config fails at runtime. The config is engineer-controlled through migrations, so injection isn't the threat model, and I added a health check on the results table.
>
> **Rollout.** About 1,500 lines for the framework, then I rolled it across eight subject areas.
>
> **My own flaw.** At production scale I noticed that readiness was per subject area: about fifty persistently failing merchants, around four percent, blocked all thirty-five thousand. I'd designed that. I wrote an ADR with four options: a VARIANT column with per-row functions, which disables predicate pushdown on a fifty-million-row table; VARIANT plus flatten, which hits a per-cell size cap; a new per-merchant table, which needs new infrastructure; and my choice, reusing the results table with a summary row plus per-merchant failure rows. The safety argument is "strictest wins": the read checks table-level failure first, so mixed old and new procedures are always safe. Since 96 percent of checks pass, storing only failures is nearly free.
>
> **Status.** Merchant-level readiness is designed, reviewed, and proven in one subject area; the broader rollout is sequenced behind net settlement.

</details>

## 4. 适用 LP 与改角度

| LP | 开场一句 | 重点讲 | 避免 |
|---|---|---|---|
| **Invent and Simplify** (P) | "Adding a validation went from 'write a task, review, deploy' to 'insert a row'." | 配置驱动；握手变 SQL 条件 | 把 ADR 状态说成已上线 |
| **Insist on the Highest Standards** (P) | "Downstream should never read half-validated data, so I made that a join condition, not a Slack convention." | trigger-status 握手；strictest-wins | — |
| **Earn Trust** (P) | "I found the flaw in my own design and wrote the ADR myself before anyone asked." | 公开自批；四方案否决理由外化；可被独立验证 | 夸大成「大家夸我」 |
| **Frugality** (P) | "Only failures are stored: at worst about 800K rows a month instead of 2.4 million a day." | 复用现有结果表、零新基础设施；容量论证 | — |
| **Are Right, A Lot** (S) | "I treated my own abstraction like someone else's code and wouldn't approve it." | disconfirm 自己；strictest wins 的正确性论证 | — |
| **Have Backbone** (S) | "The easy path was to leave the design; I pushed for the rework." | 对自己设计的反对 | 这不是「与他人分歧」，被追问时诚实说 |
| **Think Big** (S) | "It's not a feature; it's a platform other people plug into." | 8 次铺开；下游消费 | 无需求说明的「愿景」 |
| **Hire and Develop** (S) | "Standards spread through the framework, not through my reviews." | 框架/ADR/onboarding doc 传递标准 | 无 code-review 痕迹，别声称 |

## 5. 追问（≥5）

1. **Why dynamic SQL, isn't that risky?**
   - 这是 **config-driven 的代价**；配置经 **migration** 控制，不是用户输入。
   - 真风险：失去**静态检查**。
   - 缓解：**exception handler** + 结果表**健康检查**。
2. **Why a status table, not task dependencies?**
   - 下游在**不同库/不同账号**。
   - **复制的状态行**是跨边界的最低公约数；`AFTER` 依赖不跨账号。
3. **Correctness argument for merchant-level?**
   - **Strictest wins**：先判 `NOT EXISTS(表级失败)`，再判 `NOT EXISTS(商户级失败)`。
   - 未改造的 procedure 退化成**表级阻塞** = 今天的行为。
4. **Why not VARIANT?**
   - secure view 上逐行 UDF / VARIANT 解析会**关闭谓词下推**。
   - VARIANT **16 MB/cell** 上限（~98K 商户）。
   - **扁平行 + 等值 JOIN** 保留剪枝。
5. **What's the actual status?**
   - 框架 + **8 次铺开**在生产。
   - 商户级：**designed, reviewed, proven in one area**（TRANSFERS，16 个月）。
   - 全框架铺开 **sequenced behind net-settlement**。
6. **What did you learn / what changed in how you work?**
   - **粒度**是随规模要重新审视的设计参数。
   - 修自己的缺陷走比修别人 bug 更**正式的流程（ADR）**。
   - 设计任何 gate 先问「失败的**爆炸半径**是谁」。
7. **Did anyone disagree?**
   - 【待 Chi 补：ADR 评审里有没有人提出异议、你如何回应——没有就如实说「review 无实质异议」，不要编冲突】
8. **How many teams use it?**
   - 【待 Chi 补：除 Snowglobe 团队外有无其他团队接入】

## 6. 证据边界

ADR Confluence 2894288991（Proposed）；`HAS_MERCHANT_DETAIL` **不在代码里**；不说「改成了」。PR #1997 + 铺开 #2061/#2069/#2075/#2091/#2106/#2558/#3040/#3237。

## 7. Senior 升级点（bar = senior）

当前档位：**mechanism + trade-off with data 是 senior 级**（框架、ADR 四方案、strictest-wins、容量分析）；**influence 与 raise-the-bar 的证据偏薄**，且 ADR 是 Proposed。
- 把 Think Big 讲实：这是别人往上接的平台，不是 feature——【待 Chi 补：除你之外谁添加过 config 行？几次？（"someone else added a check by inserting a row without asking me" 是核心证据）】
- 把 influence 讲实：【待 Chi 补：ADR 评审时谁（职级、团队）是主要评审，提了什么问题，你如何改动 ADR？是否有人最初反对"改自己刚铺开的框架"？】
- Disagree-and-commit 素材（若有）：【待 Chi 补：评审里有没有一条你没被采纳的意见、你仍然执行了？没有就不要编，用 S6/S3 做 Backbone。】
- 状态口径永远带上（Proposed / one area proven），这本身是 senior 的诚实。
