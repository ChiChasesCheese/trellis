# M1 · Onboarding doc + 带新人 + 标准传播（Hire and Develop 的唯一素材）

> 来源：`core/Answers.md` Q6、Q13、Q16、Q23；S6（接手实习生项目）。**没有 `core/stories/` 独立笔记。**
> 主 LP：**Hire and Develop the Best**（目前唯一）；副：Earn Trust · Insist on the Highest Standards · Strive to be Earth's Best Employer · Ownership。

> [!warning] 证据边界（Answers Q13，原文）
> 没有可举证的 code-review 痕迹；**只讲 domain-ownership / architectural collaboration**，不讲"我 review 了他哪个 PR"、不编 1:1 细节。真实可查的连接点：他的 exclusion service 架构上依赖我的平台消费同一批上游事件。

## 1. 可用事实

| 事实 | 来源 |
|---|---|
| 带的是一位新人工程师，他的三块工作：定价服务里的 **Snowglobe exclusion service**（防止对已迁移商户重复计费）、出款服务 → 定价服务的 **journaling-schedule gRPC 同步**、**scheme fee 估算 ML**；每一块都接入/依赖我的费用平台 | Answers Q13 |
| 我做的：把领域边界、契约、正确性标准前置定义清楚（哪些商户在什么记账状态下算已迁移；下游需要什么 schema、什么一致性）；按下游怎么消费同一批事件来审他的设计；事故里当他依赖的 fee-calc 权威 | Answers Q13 |
| 另外接手并重新 scope 了一个实习生的 ML 项目 | Answers Q13 / S6 |
| **onboarding doc**：2024 年建，至今维护 | Answers Q6 / Q16 |
| 标准传播：质量门禁框架铺开八次 = 强制传播；ADR 展示决策如何被论证 | Answers Q16 / S2 |
| review 本身看三件事：正确性、领域边界（接缝上事件与键的语义、重试会怎样）、"strictest wins" 式安全论证 | Answers Q16 |
| 规划：让团队在没有我在场时也能处理 fee-calc 事故（从最可靠的单点到 multiplier） | Answers Q23 |
| 没有：新人的成长结果（他独立 own 了什么）、onboarding doc 的使用者数、被带者反馈 | 【待 Chi 补】 |

## 2. 60–90 秒（口述提纲）

**"I raise the bar by defining the contract first and reviewing designs by how downstream consumes them; I can't claim a code-review trail, so here is what I actually did."**

**S · Situation**
- Domain knowledge of the **fee platform** sat with **me**: a single point.
- A newer engineer's **three pieces** all plug into the platform I own: an **exclusion service**, a **gRPC journaling-schedule sync**, and a **scheme-fee ML estimator**.

**T · Task**
- Make the platform usable **without me in the room**: new people can start, and his work stays **correct** against my domain.

**A · Action** (dated step first; the other dates aren't in my sources)
1. In **2024** I wrote the team's **onboarding doc**, and I still maintain it.
2. For the mentee, I **defined boundaries up front**: which merchants count as **migrated** in which accounting state.
3. I also defined the **schema and consistency** the downstream needs.
4. I reviewed his designs by asking **how the same upstream events are consumed on my side**.
5. In incidents, I was the **fee-calc authority** he could depend on.
6. I built the **quality-check framework** so standards spread as the **easiest path**, not through my reviews.

**R · Result**
- The quality-check framework rolled out **eight times**, which forces standards to spread.
- 【待 Chi 补：新人现在独立 own 了什么、onboarding doc 帮助过几个人上手】

**L · Learning / Mechanism**
- **Contract first**, then review by downstream consumption.
- **Doc, framework, ADR**: mechanisms, not my personal reviews.

<details><summary>逐字稿（参考，不背）</summary>

> I wrote the team's onboarding doc in 2024 and I still maintain it. I also mentor a newer engineer on the team, and his three pieces of work — an exclusion service that prevents double-billing merchants who've migrated, a gRPC sync of payout journaling schedules into the pricing service, and an ML estimator for scheme fees — all plug into the fee platform I own. I can't claim a code-review trail, so here's what I did: I defined the boundaries up front — which merchants count as migrated in which accounting state, what schema and what consistency the downstream needs — and reviewed his designs by asking how the same upstream events would be consumed on my side. In incidents, I was the fee-calc authority he could depend on.
>
> And I built the quality-check framework so that standards spread by being the easiest path rather than through my reviews. 【待 Chi 补：新人现在独立 own 了什么、onboarding doc 帮助过几个人上手】

</details>

## 3. 2 分钟（口述提纲）

**"I raise the bar by defining the contract first and reviewing designs by how downstream consumes them; I can't claim a code-review trail, so here is what I actually did."**

**S · Situation**
- **Why this matters**: domain knowledge concentrated in me, a **single point** (the plan: from most reliable single point to **multiplier**).
- A newer engineer's three pieces all connect to my **fee platform**.

**T · Task**
- Build **mechanisms** so the team handles fee-calc work and incidents **without me**.
- Make his work **correct** against my domain boundaries.

**A · Action** (dated step first; the other dates aren't in my sources)
1. **Onboarding doc**, written in **2024**, still maintained.
2. Mentee piece one: an **exclusion service** that prevents **double-billing migrated merchants**.
3. Piece two: a **gRPC sync** of payout **journaling schedules** into the pricing service. Piece three: a **scheme-fee ML estimator**.
4. I **defined boundaries and contracts up front**: which merchants count as migrated, in which accounting state.
5. I defined the **schema and consistency** the downstream needs.
6. I reviewed designs by **how downstream consumes the same events**, plus correctness and retry behavior.
7. In incidents, I was the **fee-calc authority** he depended on.
8. **Quality-check framework** (rolled out eight times) and **ADRs** carry the standards.
9. I also **took over and re-scoped an intern's ML project**.

**R · Result**
- 【待 Chi 补：可数结果，例如"他的服务上线了"/"他独立处理过一次事故"】

**L · Learning / Mechanism**
- **Mechanisms** over heroics: onboarding doc, framework, ADR, **contract first**.
- What I'd do differently: 【待 Chi 补】

<details><summary>逐字稿（参考，不背；2 分钟版原为结构列表，无逐字稿）</summary>

> 1. **Why this matters**：领域知识集中在我一个人 → 单点（Answers Q23 的"从最可靠的单点到 multiplier"）。
> 2. **Mechanisms**：onboarding doc、框架、ADR、契约先行。
> 3. **The mentee**：三块工作 + 我定义的边界。
> 4. **Result**：【待 Chi 补：可数结果，例如"他的服务上线了"/"他独立处理过一次事故"】
> 5. **What I'd do differently**：【待 Chi 补】

</details>

## 4. 适用 LP 与改角度

| LP | 开场一句 | 重点讲 | 避免 |
|---|---|---|---|
| **Hire and Develop the Best** (P) | "I raise the bar by defining the contract first and reviewing designs by how downstream consumes them." | 契约先行；onboarding doc；接手实习生项目 | 编 1:1、编 PR review |
| **Earn Trust** (S) | "He could depend on me being the authority during an incident." | 事故里的权威 | — |
| **Insist on the Highest Standards** (S) | "Standards spread because the framework makes them the easiest path." | 框架/ADR | — |
| **Strive to be Earth's Best Employer** (S, 薄) | "I wrote the onboarding doc so the next person doesn't need me to start." | onboarding；知识不再单点 | 不要声称 DEI/福祉类贡献——没有证据 |

## 5. 追问（≥5）

1. **How did you help him grow, concretely?**
   - **Boundaries and contracts up front**.
   - Reviewed designs by **downstream consumption**.
   - **Incident authority** he could rely on.
   - **No 1:1 details.**
2. **What did he disagree with you on?**
   - 【待 Chi 补：一次他提出不同意见、你改变了想法的例子】
3. **What happened to his projects?**
   - 【待 Chi 补】
4. **What's in the onboarding doc?**
   - 【待 Chi 补：目录/结构，使用者反馈】
5. **How do you give feedback?**
   - 【待 Chi 补：一个真实的反馈场景】
6. **A time you raised the bar for hiring/promotion?**
   - 【待 Chi 补：是否参与过面试/评级；没有就如实说"没有，我的影响是通过框架和文档"】
7. **What if someone doesn't improve?**
   - 【待 Chi 补】

## 6. Senior 升级点（bar = senior）

当前档位：**这是整个题库里最低于 senior 的一块**：senior 要求带教有可见产出（带的人独立 own 了什么、你让团队的标准提高了什么）。
- 【待 Chi 补（最高优先级，Chi 本人确认后才能进入口播）：新人现在 own 的东西；onboarding doc 的受益者；你做过的 code review / 设计评审的一个真实例子（含你提的意见与对方的改动）】
- 如果补不出，LP6 题库的 fallback = "诚实坦白 + 框架与 ADR 作为杠杆"（见 `../question_bank.md` LP6）。
