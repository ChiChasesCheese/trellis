---
id: nr-amz-m1-hook
node: amazon.m1
type: qa
step: 1
---
## Q
【M1 · Onboarding doc + 带新人 + 标准传播（Hire and Develop 的唯一素材）】开场第一句是什么？适用哪些 LP？要报哪些数字？

## A
**I raise the bar by defining the contract first and reviewing designs by how downstream consumes them; I can't claim a code-review trail, so here is what I actually did.**

**适用 LP**

- 主：**Hire and Develop the Best**（目前唯一）
- 副：Earn Trust、Insist on the Highest Standards、Strive to be Earth's Best Employer、Ownership
- 说话边界：没有可举证的 code-review 痕迹；只讲 domain-ownership / architectural collaboration，不讲「我 review 了他哪个 PR」，不编 1:1 细节。真实可查的连接点：他的 exclusion service 架构上依赖我的平台消费同一批上游事件

**数字**

- **onboarding doc**：**2024** 年建，至今维护
- 带的新人有 **3 块工作**：定价服务里的 **Snowglobe exclusion service**（防止对已迁移商户重复计费）、出款服务 → 定价服务的 **journaling-schedule gRPC 同步**、**scheme fee 估算 ML**；每一块都接入我的费用平台
- quality-check 框架铺开 **8 次** = 强制传播标准
- 另外接手并重新 scope 了一个**实习生的 ML 项目**
- review 看三件事：正确性、领域边界（接缝上事件与键的语义、重试会怎样）、"strictest wins" 式安全论证
- 【待补：新人现在独立 own 了什么；onboarding doc 帮助过几个人上手】
