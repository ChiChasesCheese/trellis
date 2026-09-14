---
id: reliability-chaos-hypothesis
node: reliability.resilience.containment
type: qa
---
## Q
What separates chaos engineering from "randomly breaking things in prod," and what are the steps of a proper experiment?

## A
Chaos engineering is **hypothesis testing** about resilience, not vandalism:

1. Define a **steady-state metric** (e.g. checkout success rate).
2. State the hypothesis: "if we kill 1 AZ / inject 300ms latency into service X, steady state holds."
3. Inject the fault with **minimal blast radius** (small % of traffic, one cell) and an automatic **abort condition** that stops the experiment on SLI regression.
4. If steady state breaks, you found a real weakness cheaply; fix, then widen the blast radius.

Run in production (staging lacks real traffic and real config), but only after the experiment survives staging.

## Q zh
什么将 chaos engineering 与"在生产环境中随意破坏东西"分开，一个适当的实验步骤是什么？

## A zh
Chaos engineering 是关于 resilience 的**假设测试**，不是破坏行为：

1. 定义一个**稳定状态指标**（例如 checkout 成功率）。
2. 陈述假设："如果我们杀掉 1 个 AZ / 注入 300ms 延迟到服务 X，稳定状态保持"。
3. 注入故障使用**最小爆炸半径**（小 % 的流量，一个 cell），并自动**中止条件**在 SLI 回归时停止实验。
4. 如果稳定状态破裂，你便宜地发现了真实弱点；修复，然后扩大爆炸半径。

在生产中运行（staging 缺乏真实流量和真实配置），但仅在实验在 staging 中存活后。
