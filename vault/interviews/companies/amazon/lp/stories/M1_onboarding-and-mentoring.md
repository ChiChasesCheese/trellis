# M1 · Onboarding doc + 带新人 + 标准传播（Hire and Develop 的唯一素材）

**I raise the bar by defining the contract first and reviewing designs by how downstream consumes them; I can't claim a code-review trail, so here is what I actually did.**

## 适用 LP

- 主：**Hire and Develop the Best**（目前唯一）
- 副：Earn Trust、Insist on the Highest Standards、Strive to be Earth's Best Employer、Ownership
- 说话边界：没有可举证的 code-review 痕迹；只讲 domain-ownership / architectural collaboration，不讲「我 review 了他哪个 PR」，不编 1:1 细节。真实可查的连接点：他的 exclusion service 架构上依赖我的平台消费同一批上游事件

## 数字

- **onboarding doc**：**2024** 年建，至今维护
- 带的新人有 **3 块工作**：定价服务里的 **Snowglobe exclusion service**（防止对已迁移商户重复计费）、出款服务 → 定价服务的 **journaling-schedule gRPC 同步**、**scheme fee 估算 ML**；每一块都接入我的费用平台
- quality-check 框架铺开 **8 次** = 强制传播标准
- 另外接手并重新 scope 了一个**实习生的 ML 项目**
- review 看三件事：正确性、领域边界（接缝上事件与键的语义、重试会怎样）、"strictest wins" 式安全论证
- 【待补：新人现在独立 own 了什么；onboarding doc 帮助过几个人上手】

## S / T / A / R / L

### S
- **费用平台**的领域知识集中在**我一个人**：单点
- 一位新工程师的**三块工作**都接入我 own 的平台：**exclusion service**、**gRPC journaling-schedule 同步**、**scheme-fee ML 估算**

### T
- 让平台**不靠我在场**也能用：新人能上手，他的工作对我的领域保持**正确**
- 让团队没有我也能处理 fee-calc 事故（从最可靠的单点到 multiplier）

### A
- 2024 年写团队 **onboarding doc**，至今维护
- 对新人，**前置定义边界**：哪些商户在什么记账状态下算**已迁移**
- 同时定义下游需要的 **schema 和一致性**
- 评审他的设计时问：**同一批上游事件在我这边怎么被消费**
- 事故里做他可依赖的 **fee-calc 权威**
- 建 **quality-check 框架**，让标准成为**最容易走的路**，而不是靠我 review
- 接手并重新 scope 实习生的 ML 项目

### R
- quality-check 框架铺开 **8 次**，强制标准传播
- 【待补：新人现在独立 own 了什么；onboarding doc 帮助过几个人；可数结果，比如「他的服务上线了」「他独立处理过一次事故」】

### L
- **契约先行**，再按下游消费方式评审
- **文档、框架、ADR**：机制，而不是我个人的 review

## 追问与回答

- **How did you help him grow, concretely?**
  - **前置边界和契约**；按**下游消费**评审设计；事故里的**权威**；不讲 1:1 细节
- **What did he disagree with you on?**
  - 见待补
- **What happened to his projects?**
  - 见待补
- **What's in the onboarding doc?**
  - 见待补
- **How do you give feedback?**
  - 见待补
- **A time you raised the bar for hiring/promotion?**
  - 见待补；没参与过就如实说「没有，我的影响是通过框架和文档」
- **What if someone doesn't improve?**
  - 见待补

## 换个 LP 讲

- **Hire and Develop the Best**：契约先行、onboarding doc、接手实习生项目；别编 1:1、别编 PR review
- **Earn Trust**：他可以依赖我在事故里的权威
- **Insist on the Highest Standards**：标准因为框架/ADR 成为最容易的路径而扩散
- **Strive to be Earth's Best Employer**（薄）：写 onboarding doc 让下一个人不需要我就能开始；知识不再单点；不要声称 DEI/福祉类贡献

## 待补

- 【待补（最高优先级）：新人现在 own 的东西；onboarding doc 的受益者；一个真实的 code review / 设计评审例子（含你提的意见与对方的改动）；补不出就走 LP 诚实坦白 + 框架与 ADR 作为杠杆】
- 【待补：一次他提出不同意见、你改变了想法的例子】
- 【待补：他的项目后来怎样】
- 【待补：onboarding doc 的目录/结构、使用者反馈】
- 【待补：一个真实的反馈场景】
- 【待补：是否参与过面试/评级；没有就如实说】
- 【待补：有人没进步时你怎么做】
- 【待补：What I'd do differently】

<details><summary>逐字稿</summary>

> I wrote the team's onboarding doc in 2024 and I still maintain it. I also mentor a newer engineer on the team, and his three pieces of work — an exclusion service that prevents double-billing merchants who've migrated, a gRPC sync of payout journaling schedules into the pricing service, and an ML estimator for scheme fees — all plug into the fee platform I own. I can't claim a code-review trail, so here's what I did: I defined the boundaries up front — which merchants count as migrated in which accounting state, what schema and what consistency the downstream needs — and reviewed his designs by asking how the same upstream events would be consumed on my side. In incidents, I was the fee-calc authority he could depend on.
>
> And I built the quality-check framework so that standards spread by being the easiest path rather than through my reviews.

</details>
