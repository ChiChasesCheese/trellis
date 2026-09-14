---
id: reliability-config-deploy-risk
node: reliability.resilience.containment
type: qa
---
## Q
Why are config/flag changes the riskiest deploy class — behind many of the largest real outages — and what discipline fixes it?

## A
Config changes bypass everything that makes code deploys safe: they often propagate **globally and near-instantly** (no canary, no batches), skip CI/tests, feel "small" so they skip review — and one bad value (routing rule, quota, feature flag) can take down every region at once.

Fix: treat config as a deploy artifact —

- **Version-controlled and validated** (schema/lint/dry-run before apply).
- **Progressive rollout** with the same canary stages as code, never global-at-once.
- **Automatic rollback triggers**: the rollout system watches SLIs and reverts on regression without waiting for a human.

## Q zh
为什么 config/flag 变更是最危险的部署类别——许多最大真实事故背后——什么纪律解决它？

## A zh
Config 变更绕过了让代码部署安全的一切：它们经常**全局且瞬间传播**（没有 canary，没有批次），跳过 CI/测试，感觉"小"所以跳过审查——一个坏值（routing 规则、quota、feature flag）可以同时击倒每个区域。

修复：将 config 视为部署工件——

- **版本控制和验证**（apply 前 schema/lint/dry-run）。
- **逐步推出**使用与代码相同的 canary 阶段，永远不全局一次。
- **自动回滚触发器**：推出系统监视 SLI 并在回归时自动还原，无需等待人类。
