# R2 · AI-native 迁移：Ruby/Kotlin → Snowflake/Java（Claude Code 工作流）

**The agent proposes, tests decide: I migrated legacy Ruby and Kotlin logic to Snowflake and Java with Claude Code, and held it to behavioral parity.**

## 适用 LP

- 主：**Bias for Action**、**Learn and Be Curious**
- 副：Deliver Results、Insist on the Highest Standards、Invent and Simplify

## 数字

- PayPal，2025-02 至今
- 迁移对象：legacy **Ruby / Kotlin** 业务逻辑 → **Snowflake / Java**
- 方法：AI-native 工作流，**Claude Code** 做 code review、测试生成、重构
- 质量手段：全面测试保证 **behavioral parity**
- AI 代码信任原则：**plan with the agent → TDD every phase → CI + monitoring gates**；"focus on gates and thresholds, not lines of code"；money code 里我读每个 diff
- 日常并行跑 Claude Code / Codex / Cursor；schema pool 让多个 agent 会话并行跑迁移与集成测试
- 【待补：迁移规模（多少规则/服务/行）、周期、parity 测试通过率、加速倍数；没有精确数字就给可数事实】

## S / T / A / R / L

### S
- PayPal 费用平台，**2025-02 至今**：legacy **Ruby/Kotlin** 业务逻辑
- 【待补：迁移的具体对象与规模，例如「X 个规则 / Y 个服务 / Z 行」，以及为什么必须搬】

### T
- 迁到 **Snowflake/Java**，保证 **behavioral parity**
- 用 **AI-native 工作流**更快交付，而不是把 AI 当自动补全

### A
- 用 **Claude Code** 做 **code review、测试生成、重构**
- 用**全面测试**保证 parity
- 我的 agent 规则：**先和 agent 规划阶段**，每阶段 **TDD**，让 **CI 和监控 gate** 抓回归
- 这是 money code，所以**每个 diff 我自己读**

### R
- 通过全面测试达到 **behavioral parity**，交付**加速**（简历措辞）

### L
- **Agent 提议，测试裁决，人读 diff**
- 信任 **gate 和阈值**，不看行数

## 追问与回答

- **How did you verify parity?**
  - 见待补（对拍 / 影子运行 / 表级 diff？）
- **What did the AI get wrong?**
  - 见待补；没有记录就说没有，别编
- **How do you trust AI-generated code?**
  - **Plan → TDD → CI + monitoring gates**；看 **gate 和阈值**，不看行数；**money code 我读每个 diff**
- **How much faster?**
  - 见待补
- **What did you learn about the legacy logic?**
  - 见待补
- **Would you let an agent do this unsupervised?**
  - **不**：agent 提议，**测试裁决**，人读 diff
- **Team adoption?**
  - **schema pool** 让多个会话并行；**on-call copilot** 被相邻团队采用

## 换个 LP 讲

- **Bias for Action**："AI let me move quickly, with tests deciding."：全面测试保 parity、每阶段 TDD；别说成「AI 做的」
- **Learn and Be Curious**：学会 agent 哪里可信哪里不可信；gate/阈值、money code 逐 diff 读；别夸大工具
- **Deliver Results**：等有基线和数字再讲（见待补）
- **Insist on the Highest Standards**：bar 是 behavioral parity，不是「看着对」；parity 测试

## 待补

- 【待补：迁移的具体对象与规模】
- 【待补：parity 测试具体怎么做：先写测试固定旧行为？影子对拍？】
- 【待补：结果：parity 测试通过情况、发现几个旧逻辑里的隐藏行为、交付时间比预期短多少（给基线）】
- 【待补：是否 parity-test-first，被否决的备选是什么】
- 【待补：AI 做错的一个真实例子】
- 【待补：这套 AI-native + parity-test 流程有没有被队友复用】
- 【待补：迁移中与资深同事/其他团队的分歧点（若有）】
- 【待补：一个你拒绝 AI 建议的决定】
- 【待补：What I'd do differently】

<details><summary>逐字稿</summary>

> I migrated legacy Ruby and Kotlin business logic into Snowflake and Java, and I did it with an AI-native workflow rather than treating AI as autocomplete. The rule I worked by: the agent proposes, tests decide. I used Claude Code for code review, test generation and refactoring, and I ensured behavioral parity through comprehensive testing. My general rule with agents is to plan the phase with them, do TDD for each phase, and let CI and monitoring gates catch regressions. Because this is money code, I read every diff myself.

</details>
