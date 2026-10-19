---
id: nr-amz-r2-followups
node: amazon.r2
type: qa
step: 3
---
## Q
【R2 · AI-native 迁移：Ruby/Kotlin → Snowflake/Java（Claude Code 工作流）】面试官会追问什么？每个怎么答？

## A
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
