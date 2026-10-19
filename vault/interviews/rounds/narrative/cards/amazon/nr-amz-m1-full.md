---
id: nr-amz-m1-full
node: amazon.full
type: qa
step: 12
---
## Q
<p class="title">新人 onboarding 与带教<span class="meta">01 完整故事</span></p>

先在心里把前因后果过一遍，再用英文完整讲一遍。

## A
<span class="label">前因后果</span>

- 背景：费用平台的领域知识集中在我一个人身上，是单点。同时，团队里一位新工程师的三块工作都要接入我 own 的平台：防止对已迁移商户重复计费的 exclusion service、出款服务到定价服务的 journaling-schedule gRPC 同步、scheme fee 估算 ML。
- 目标：让平台不靠我在场也能用，让新人能上手、他的工作对我的领域保持正确，让团队没有我也能处理 fee-calc 事故。
- 我做了什么（文档和契约）：2024 年写了团队 onboarding doc，至今维护；对新人前置定义边界，比如哪些商户在什么记账状态下算已迁移，以及下游需要的 schema 和一致性；评审他的设计时，我问的是同一批上游事件在我这边怎么被消费。
- 我做了什么（机制）：事故里做他可以依赖的 fee-calc 权威；建 quality-check 框架，让标准成为最容易走的路，而不是靠我逐个 review；还接手并重新 scope 了一个实习生的 ML 项目。
- 结果与学到：quality-check 框架铺开了 8 次，标准因此传播。我不能声称有 code-review 记录，所以我的杠杆是契约先行，加上文档、框架和 ADR 这些机制，而不是我个人在场。

<span class="label">英文口述（60–90 秒）</span>

I wrote the team's onboarding doc in 2024 and I still maintain it. I also mentor a newer engineer on the team, and his three pieces of work, an exclusion service that prevents double-billing merchants who've migrated, a gRPC sync of payout journaling schedules into the pricing service, and an ML estimator for scheme fees, all plug into the fee platform I own. I can't claim a code-review trail, so here's what I did: I defined the boundaries up front, which merchants count as migrated in which accounting state and what schema and consistency the downstream needs, and I reviewed his designs by asking how the same upstream events would be consumed on my side. In incidents, I was the fee-calc authority he could depend on. And I built the quality-check framework, now rolled out eight times, so that standards spread by being the easiest path rather than through my reviews.

<div class="sources"><b>表达 · business English</b><br>• <b><i>single point of failure</i></b> — 单点故障（知识集中在一人）<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Fee-platform knowledge sat with me, which made me a single point of failure.”</span><br>• <b><i>ramp up</i></b> — 上手、进入状态<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The onboarding doc helps a new engineer ramp up without me in the room.”</span><br>• <b><i>contract first</i></b> — 契约先行<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I go contract first: boundaries and schema before any design review.”</span></div>
