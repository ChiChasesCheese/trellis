---
id: nr-amz-m1-starl
node: amazon.m1
type: qa
step: 2
---
## Q
【M1 · Onboarding doc + 带新人 + 标准传播（Hire and Develop 的唯一素材）】STAR-L 提纲（60–90 秒）

## A
**S**

- **费用平台**的领域知识集中在**我一个人**：单点
- 一位新工程师的**三块工作**都接入我 own 的平台：**exclusion service**、**gRPC journaling-schedule 同步**、**scheme-fee ML 估算**

**T**

- 让平台**不靠我在场**也能用：新人能上手，他的工作对我的领域保持**正确**
- 让团队没有我也能处理 fee-calc 事故（从最可靠的单点到 multiplier）

**A**

- 2024 年写团队 **onboarding doc**，至今维护
- 对新人，**前置定义边界**：哪些商户在什么记账状态下算**已迁移**
- 同时定义下游需要的 **schema 和一致性**
- 评审他的设计时问：**同一批上游事件在我这边怎么被消费**
- 事故里做他可依赖的 **fee-calc 权威**
- 建 **quality-check 框架**，让标准成为**最容易走的路**，而不是靠我 review
- 接手并重新 scope 实习生的 ML 项目

**R**

- quality-check 框架铺开 **8 次**，强制标准传播
- 【待补：新人现在独立 own 了什么；onboarding doc 帮助过几个人；可数结果，比如「他的服务上线了」「他独立处理过一次事故」】

**L**

- **契约先行**，再按下游消费方式评审
- **文档、框架、ADR**：机制，而不是我个人的 review
