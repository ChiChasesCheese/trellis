---
id: nr-amz-r2-starl
node: amazon.outline
type: qa
step: 41
---
## Q
<p class="title">AI-native 迁移<span class="meta">02 提纲</span></p>

STAR-L 提纲（60–90 秒）

## A
<span class="label">S</span>

- PayPal 费用平台，**2025-02 至今**：legacy **Ruby/Kotlin** 业务逻辑
- 【待补：迁移的具体对象与规模，例如「X 个规则 / Y 个服务 / Z 行」，以及为什么必须搬】

<span class="label">T</span>

- 迁到 **Snowflake/Java**，保证 **behavioral parity**
- 用 **AI-native 工作流**更快交付，而不是把 AI 当自动补全

<span class="label">A</span>

- 用 **Claude Code** 做 **code review、测试生成、重构**
- 用**全面测试**保证 parity
- 我的 agent 规则：**先和 agent 规划阶段**，每阶段 **TDD**，让 **CI 和监控 gate** 抓回归
- 这是 money code，所以**每个 diff 我自己读**

<span class="label">R</span>

- 通过全面测试达到 **behavioral parity**，交付**加速**（简历措辞）

<span class="label">L</span>

- **Agent 提议，测试裁决，人读 diff**
- 信任 **gate 和阈值**，不看行数

<div class="sources"><b>表达 · business English</b><br>• <b><i>plan with the agent</i></b> — 先和 agent 一起做规划<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I plan each phase with the agent before any code is written.”</span><br>• <b><i>catch regressions</i></b> — 抓住回归问题<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“CI and monitoring gates catch regressions before they reach production.”</span><br>• <b><i>phase by phase</i></b> — 分阶段推进<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I migrated phase by phase, with TDD in every phase.”</span></div>
