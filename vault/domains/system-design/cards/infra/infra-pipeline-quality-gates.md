---
id: infra-pipeline-quality-gates
node: infra.delivery
type: qa
---
## Q
Why order CI/CD pipeline stages as progressively more expensive quality gates, and what class of failure does each stage uniquely catch?

## A
Each stage should catch what is **cheapest to catch there**; the ordering exists so most failures die in seconds, not in production.

- **Build + unit tests** (seconds–minutes): logic errors, type/contract breaks.
- **Integration & contract tests** (minutes): wiring and API compatibility between services.
- **Staging / e2e**: environment-shaped bugs — config, migrations, cross-service flows.
- **Production canary**: the only gate with real traffic, real data, real scale — catches what no pre-prod environment can.

Design point: the pipeline *is* the release process. Any change that bypasses it (a manual config flip, an ad-hoc migration) is an ungated deploy.

## Q zh
为什么作为渐进式更昂贵的质量门排序 CI/CD 流水线阶段，以及什么类失败各阶段独特地抓住？

## A zh
各阶段应该抓住**在那里最便宜抓住**什么；排序存在以便大多数失败在秒内死亡，不是在生产。

- **构建 + 单元测试**（秒-分钟）：逻辑错误、类型/契约破裂。
- **集成 & 契约测试**（分钟）：服务之间的布线和 API 兼容性。
- **Staging / e2e**：环境形状的 bug——配置、迁移、跨服务流。
- **生产 canary**：仅有真实流量、真实数据、真实规模的门——抓住无 pre-prod 环境能抓住的。

设计点：流水线**就是**发布过程。任何绕过它的改变（手动配置翻转、ad-hoc 迁移）是无门部署。
