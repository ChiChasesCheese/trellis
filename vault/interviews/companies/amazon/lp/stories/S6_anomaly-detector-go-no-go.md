# S6 · Fee anomaly detector 的 go/no-go（判断力 · 说不 · 分阶段）

> 来源：`core/stories/S6 Anomaly detector go-no-go.md`（status: verified）。
> 主 LP：**Are Right, A Lot · Dive Deep · Have Backbone · Ownership**；副：Frugality · Invent and Simplify · Bias for Action · Deliver Results · Insist on the Highest Standards。
> 一句话：*"I inherited a departing intern's ML detector that had only run in QA, and instead of momentum I wrote a go/no-go that split it into a safe SQL phase and a gated ML phase."*

## 1. 数字（⚠️ 来自我自己的评估文档，尚未从生产复核）

| 数字 | 口播写法 |
|---|---|
| QA 6 个合成商户 vs 生产 18,140 商户 | "six synthetic merchants versus eighteen thousand" |
| QA 8.3 亿行 vs 生产 390 亿行 | "under a billion rows versus tens of billions" |
| 峰值一天 7.6 亿行 | "up to about 760 million rows on a peak day" |
| 1,468 plan code · 15,293 (plan, description) 组合 | "about fifteen thousand plan combinations" |
| 5–8 人周编码 · 2–3 个月到生产可信 | Phase 2 估计 |
| 99.5% 阈值 × 每天数亿行 = 每天数百万条告警 | 告警量风险 |
| 唯一不可再生的是分析师 disposition 标注 | 离职前导出 |

## 2. 60–90 秒口述提纲

**I inherited a departing intern's ML detector, and instead of momentum I wrote a go/no-go that split it into a safe SQL phase and a gated ML phase.**

**S · Situation**
- A leaving **intern** left an ML **fee-anomaly detector** that had only ever run in **QA**.

**T · Task**
- Decide: keep building, or **assess** — and decide what had to **survive** their departure.

**A · Action** (in the order it happened)
1. Wrote a **go/no-go assessment** instead of continuing to build.
2. Compared **QA vs production**: six synthetic merchants vs ~**18,000**; under a billion rows vs **tens of billions**; ~**760M** rows on a peak day.
3. Saw the **per-row numpy** serving would time out at that scale — QA could never show it.
4. Split **what dies** with the departure from what is **reproducible**; got the analysts' **labels** exported before the last day.
5. Phased it: **Phase 1** the deterministic rule as pure **SQL**; **Phase 2** ML retrain, 2–3 months, behind a **gate**.
6. **Froze** the Slack alerting and CI/CD work until the gate says go.

**R · Result**
- The irreplaceable **labels are safe**; the cheap defensive layer has a clear path.
- Numbers come from **my own assessment**, not yet re-verified on production.

**L · Learning / Mechanism**
- A **written gate** my manager can audit; I'd rather stop a project than ship one that pages the team at **3 a.m.**

<details><summary>逐字稿（参考，不背）</summary>

> I inherited an ML fee-anomaly detector from an intern who was leaving. It had only ever run in QA. The easy path was to keep building. Instead I wrote a go/no-go assessment. QA had six synthetic merchants and under a billion rows; production is eighteen thousand merchants, around fifteen thousand plan combinations, and up to about 760 million rows on a peak day. The serving design was a per-row numpy forward pass, which would time out at that scale, and QA could never have shown it.
>
> I split the problem. What disappears when the intern leaves versus what's reproducible from code: only the analysts' labels were irreplaceable, so I got those exported before their last day. Then a phased plan. Phase one ships only the deterministic consistency rule — amount equals rate times quantity plus fixed — as pure SQL, which Snowflake handles at billions of rows. Phase two, retraining and a new serving design, is two to three months and sits behind an explicit go/no-go gate. I froze the Slack alerting and CI/CD work until the gate says go. I'd rather stop a project than ship one that pages the team at 3 a.m.

</details>

## 3. 2 分钟口述提纲

**I inherited a departing intern's ML detector, and instead of momentum I wrote a go/no-go that split it into a safe SQL phase and a gated ML phase.**

**S · Situation**
- The intern left a **three-layer detector**: autoencoder (PyTorch train, numpy inference), plan-deviation features, **deterministic rules**; five sources, deployed **by hand**.
- Nobody had ever seen it on **production data**.

**T · Task**
- Mine to decide: **keep building**, or stop and **assess**.

**A · Action** (in the order it happened)
1. Wrote a **State / Handoff / Prod-Cutover** assessment instead of pushing on.
2. Found QA: **6 synthetic merchants**, the first two **97%** of ~830M rows; production: **18,140 merchants**, **15,293** plan-and-description combinations, ~**39B** rows.
3. Flagged three risks: per-row numpy **times out**; precision unknowable without ground truth (**shadow mode** only); a 99.5% threshold means **millions of alerts a day**.
4. Exported the **analysts' disposition labels** — the one irreplaceable asset — before the last day.
5. Planned **Phase 1** (deterministic rule, SQL pushdown, a few weeks) and **Phase 2** (ML retrain and inference, **2–3 months**, behind a business-driver gate).
6. **Froze** alerting and CI/CD work until the gate says go; wrote it all down so my manager could **judge independently**.

**R · Result**
- Labels **safe**, the cheap defensive layer has a path, and the team's time went to a real **P1**.
- Cost I accepted: I said **no** to a quick win and delayed visible output.
- The numbers are from my own assessment, not re-verified on production — I'd say so.

**L · Learning / Mechanism**
- I turned a hunch ("this won't scale") into a **written gate** my manager could audit.
- **What I'd do differently:** 【待 Chi 补：What I'd do differently（原稿未写）】

<details><summary>逐字稿（参考，不背）</summary>

> **Situation.** An intern left behind a three-layer detector: an autoencoder trained in PyTorch with numpy inference, plan-deviation features, and deterministic consistency rules, with five data sources each having its own model and daily scoring procedure, deployed by hand. Nobody had ever seen it on production data.
>
> **The decision that was mine.** Keep building, or stop and assess? Momentum said finish and push. I wrote a State / Handoff / Prod-Cutover assessment.
>
> **What I found.** QA: six synthetic merchants, the first two being 97 percent of rows, about 830 million rows. Production: 18,140 merchants, 1,468 plan codes, 15,293 plan-and-description combinations, about 39 billion rows, up to about 760 million on a peak day. A per-row numpy forward pass would time out. And the precision was unknowable without ground truth — the only option was shadow mode. At a 99.5 percent threshold times hundreds of millions of rows, it would also produce millions of alerts a day.
>
> **What I did.** First, what's irreplaceable — the analysts' disposition labels — exported before the last day. Second, a phase plan: Phase one is the deterministic rule only, as SQL pushdown, a few weeks. Phase two, the ML retrain and new inference, two to three months, behind a business-driver gate. Third, I froze alerting and CI/CD work until the gate gives a go, and wrote the whole thing down so my manager could judge it independently.
>
> **Cost I accepted.** I said no to something that looked like a quick win and delayed visible output. **Result:** the labels are safe, the cheap defensive layer has a clear path, and the team's time went to a real P1. The numbers are from my own assessment and not yet re-verified on production; I'd say that if asked.

</details>

## 4. 适用 LP 与改角度

| LP | 开场一句 | 重点讲 | 避免 |
|---|---|---|---|
| **Are Right, A Lot** (P) | "I tested the project against production reality before it shipped and found it would fail." | QA vs 生产的数量级；风险排序；制度化 gate | 把评估数字当作已验证事实 |
| **Dive Deep** (P) | "The failure wasn't in the model, it was in a numpy loop that QA could never exercise." | 逐行推理 vs set-based；分布（前两商户占 97%） | — |
| **Have Backbone** (P) | "Everyone expected me to finish and ship it; I wrote down why we shouldn't, and froze the work." | 对惯性/期待说不；用文档而非情绪 | 不是 disagree-and-commit |
| **Ownership** (P) | "The person who built it was leaving; I decided what had to survive." | 区分会丢 vs 可重建；先救标注 | — |
| **Frugality** (S) | "Two to three months of retraining wasn't worth it until a business driver said so." | 不按沉没成本排序 | 无成本数字 |
| **Invent and Simplify** (S) | "The deterministic rule needs no ML at all." | Phase 1 纯 SQL | — |
| **Bias for Action** (S) | "I got the labels exported before the last day — a one-way door." | 先保不可再生的东西 | — |

## 5. 追问（≥5）

1. **Who asked you to make this assessment?**
   - 【待 Chi 补：是自己发起还是经理要求？（影响 Ownership vs 被分配）】
2. **How did you decide it was a no-go for Phase 2 and not just 'harder'?**
   - 推理在大 warehouse 上**必然超时**。
   - 精确率**无 ground truth**。
   - 告警量 = **每天数百万条**。
   - 估算 **5–8 人周** + **2–3 月**。
3. **What was the pushback?**
   - 【待 Chi 补：有没有人希望照原计划上线？你怎么回应？】
4. **How do you know your numbers are right?**
   - 来自**我自己的评估文档**，尚未从生产复核。
   - 口播用**量级**；这是诚实边界。
5. **What happened after?**
   - Jira **DTBTTFOUND-3254 … 3261**（label `anomaly-detector`）已开。
   - Phase 1 进度：【待 Chi 补：Phase 1 是否已排期/上线、gate 当前状态】
6. **What would make you say go?**
   - **业务驱动明确** + **shadow 精确率**达到阈值。
   - 具体阈值：【待 Chi 补】
7. **Wasn't that wasted intern work?**
   - 代码 / terraform / 训练配方（**固定 seed**）都可重建。
   - 唯一不可再生的是**标注**，已导出。

## 6. Senior 升级点（bar = senior）

当前档位：**ambiguity + judgment + trade-off 已是 senior 级**；**缺 influence 与 mentoring 的侧面**。
- 【待 Chi 补：你如何把评估结论说服经理/stakeholder（会议还是文档）？谁签字冻结？（"没有权威地让别人停手"是 senior 信号）】
- 【待 Chi 补：和离职实习生的交接过程——你是否给了他反馈/带他把标注导出？（可作为 Hire and Develop 的侧证，但**不点名**，别夸大）】
- 升级句：「I turned a hunch ('this won't scale') into a written gate my manager could audit.」

## 7. 证据边界

不点名实习生；Confluence 3049697063。
