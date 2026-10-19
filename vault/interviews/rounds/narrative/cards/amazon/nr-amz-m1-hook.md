---
id: nr-amz-m1-hook
node: amazon.outline
type: qa
step: 34
---
## Q
<p class="title">新人 onboarding 与带教<span class="meta">02 提纲</span></p>

开场第一句是什么？适用哪些 LP？要报哪些数字？

## A
<span class="label">开场</span>

**I raise the bar by defining the contract first and reviewing designs by how downstream consumes them; I can't claim a code-review trail, so here is what I actually did.**

<span class="label">适用 LP</span>

- 主：**Hire and Develop the Best**（目前唯一）
- 副：Earn Trust、Insist on the Highest Standards、Strive to be Earth's Best Employer、Ownership
- 说话边界：没有可举证的 code-review 痕迹；只讲 domain-ownership / architectural collaboration，不讲「我 review 了他哪个 PR」，不编 1:1 细节。真实可查的连接点：他的 exclusion service 架构上依赖我的平台消费同一批上游事件

<span class="label">数字</span>

- **onboarding doc**：**2024** 年建，至今维护
- 带的新人有 **3 块工作**：定价服务里的 **Snowglobe exclusion service**（防止对已迁移商户重复计费）、出款服务 → 定价服务的 **journaling-schedule gRPC 同步**、**scheme fee 估算 ML**；每一块都接入我的费用平台
- quality-check 框架铺开 **8 次** = 强制传播标准
- 另外接手并重新 scope 了一个**实习生的 ML 项目**
- review 看三件事：正确性、领域边界（接缝上事件与键的语义、重试会怎样）、"strictest wins" 式安全论证
- 【待补：新人现在独立 own 了什么；onboarding doc 帮助过几个人上手】

<div class="sources"><b>表达 · business English</b><br>• <b><i>scale yourself</i></b> — 放大自己的影响力<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I scaled myself through a doc and a framework rather than reviews.”</span><br>• <b><i>bus factor</i></b> — 巴士系数（关键人缺席的风险）<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The doc raised our bus factor on the fee platform.”</span><br>• <b><i>institutional knowledge</i></b> — 沉淀在组织里的知识<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I turned institutional knowledge into a doc that outlives me.”</span></div>
