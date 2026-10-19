---
id: nr-amz-r2-starl
node: amazon.r2
type: qa
step: 2
---
## Q
【R2 · AI-native 迁移：Ruby/Kotlin → Snowflake/Java（Claude Code 工作流）】STAR-L 提纲（60–90 秒）

## A
**S**

- PayPal 费用平台，**2025-02 至今**：legacy **Ruby/Kotlin** 业务逻辑
- 【待补：迁移的具体对象与规模，例如「X 个规则 / Y 个服务 / Z 行」，以及为什么必须搬】

**T**

- 迁到 **Snowflake/Java**，保证 **behavioral parity**
- 用 **AI-native 工作流**更快交付，而不是把 AI 当自动补全

**A**

- 用 **Claude Code** 做 **code review、测试生成、重构**
- 用**全面测试**保证 parity
- 我的 agent 规则：**先和 agent 规划阶段**，每阶段 **TDD**，让 **CI 和监控 gate** 抓回归
- 这是 money code，所以**每个 diff 我自己读**

**R**

- 通过全面测试达到 **behavioral parity**，交付**加速**（简历措辞）

**L**

- **Agent 提议，测试裁决，人读 diff**
- 信任 **gate 和阈值**，不看行数
