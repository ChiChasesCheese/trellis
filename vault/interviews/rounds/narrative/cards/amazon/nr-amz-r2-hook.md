---
id: nr-amz-r2-hook
node: amazon.r2
type: qa
step: 1
---
## Q
【AI-native 迁移：Ruby/Kotlin → Snowflake/Java（Claude Code 工作流）】开场第一句是什么？适用哪些 LP？要报哪些数字？

## A
**The agent proposes, tests decide: I migrated legacy Ruby and Kotlin logic to Snowflake and Java with Claude Code, and held it to behavioral parity.**

**适用 LP**

- 主：**Bias for Action**、**Learn and Be Curious**
- 副：Deliver Results、Insist on the Highest Standards、Invent and Simplify

**数字**

- PayPal，2025-02 至今
- 迁移对象：legacy **Ruby / Kotlin** 业务逻辑 → **Snowflake / Java**
- 方法：AI-native 工作流，**Claude Code** 做 code review、测试生成、重构
- 质量手段：全面测试保证 **behavioral parity**
- AI 代码信任原则：**plan with the agent → TDD every phase → CI + monitoring gates**；"focus on gates and thresholds, not lines of code"；money code 里我读每个 diff
- 日常并行跑 Claude Code / Codex / Cursor；schema pool 让多个 agent 会话并行跑迁移与集成测试
- 【待补：迁移规模（多少规则/服务/行）、周期、parity 测试通过率、加速倍数；没有精确数字就给可数事实】
