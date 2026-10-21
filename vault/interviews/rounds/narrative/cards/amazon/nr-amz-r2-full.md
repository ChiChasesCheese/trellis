---
id: nr-amz-r2-full
node: amazon.full
type: qa
step: 14
---
## Q
<p class="title">AI-native 迁移<span class="meta">01 完整故事</span></p>

先在心里把前因后果过一遍，再用英文完整讲一遍。

## A
<span class="label">前因后果</span>

- 背景：从 2025-02 起，我在 PayPal 费用平台，要把 legacy 的 Ruby 和 Kotlin 业务逻辑迁到 Snowflake 和 Java。
- 目标：迁移后行为必须和旧系统一致（behavioral parity），同时我想用 AI-native 的工作流更快交付，而不是把 AI 当自动补全。
- 我做了什么：用 Claude Code 做 code review、测试生成和重构；规则是先和 agent 一起规划每个阶段，每个阶段做 TDD，再让 CI 和监控 gate 抓回归。因为这是 money code，每个 diff 我自己读。
- 结果：通过全面的测试达到了 behavioral parity，交付也更快了；具体倍数和规模我没有精确数字，不夸大。
- 为什么这样做：agent 只负责提议，测试负责裁决，人负责读 diff；信任的是 gate 和阈值，而不是代码行数。

<span class="label">英文口述（60–90 秒）</span>

Since February 2025 at PayPal, I migrated legacy Ruby and Kotlin business logic into Snowflake and Java, and I did it with an AI-native workflow rather than treating AI as autocomplete. The rule I worked by: the agent proposes, tests decide. I used Claude Code for code review, test generation and refactoring, and I ensured behavioral parity through comprehensive testing. My general rule with agents is to plan each phase with them, do TDD for every phase, and let CI and monitoring gates catch regressions. I focus on gates and thresholds, not lines of code. And because this is money code, I read every diff myself.

<div class="sources"><b>表达 · business English</b><br>• <b><i>behavioral parity</i></b> — 新旧系统行为完全一致<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The bar for the migration was behavioral parity, not code that merely looked right.”</span><br>• <b><i>AI-native workflow</i></b> — 以 AI 为核心环节设计的工作流<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I used an AI-native workflow, with the agent in planning, tests and refactoring.”</span><br>• <b><i>money code</i></b> — 直接处理资金的代码，容错极低<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Because it&#x27;s money code, I read every diff myself.”</span></div>
