---
id: nr-amz-r2-followups
node: amazon.followups
type: qa
step: 66
---
## Q
<p class="title">AI-native 迁移<span class="meta">03 追问</span></p>

面试官会追问什么？每个怎么答？

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

<div class="sources"><b>表达 · business English</b><br>• <b><i>shadow run</i></b> — 影子运行：新旧并行跑、只比对不生效<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“A shadow run would let me compare old and new outputs without affecting payments.”</span><br>• <b><i>pin down existing behavior</i></b> — 用测试固定住现有行为<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I&#x27;d pin down existing behavior with tests before changing anything.”</span><br>• <b><i>human in the loop</i></b> — 关键环节由人把关<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I would never run this unsupervised; a human stays in the loop on every diff.”</span></div>
