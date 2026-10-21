---
id: nr-amz-g4-followups
node: amazon.followups
type: qa
step: 91
---
## Q
<p class="title">什么时候信任 LLM<span class="meta">03 追问</span></p>

面试官会追问什么？每个怎么答？

## A
- **Tell me about a time you overrode the tool / didn't trust it.**
    - 「一个自信的错数字」（38%）、编译失败的 Java 例子、Numba（行为已变）。
    - 【待补：工作中一次你拒绝了 AI 建议的具体决定，见 「AI-native 迁移」】
- **How do you stop a teammate from over-trusting?**
    - 规则放进仓库而不是口头：gate、PR 模板、「AI 写的也要你能解释每一行」。
    - 【待补：真实带教或 code review 里的做法，见 「新人 onboarding 与带教」】
- **What's the failure of your rule?**
    - oracle 本身错（测试和代码同源盲区）→ 变异测试、独立路径对拍。
    - 以及「合理假设上的错误结论」gate 看不见。
- **Would you let an agent run unsupervised?**
    - 不：agent 提议、测试裁决、人读 diff。
    - 权限由我控制，agent 不能改自己的权限。
- **Security?**
    - 公开仓库规则（不放招聘人员姓名、邮件内容）、爆炸半径 guard、最小权限；见 [[primer]] 安全一节。



<div class="sources"><b>表达 · business English</b><br>• <b><i>override</i></b> — 否决、推翻（工具的建议）<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I overrode the agent when a figure had no primary source.”</span><br>• <b><i>single point of failure</i></b> — 单点故障<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“If the test and the code share a blind spot, the oracle becomes a single point of failure.”</span><br>• <b><i>least privilege</i></b> — 最小权限<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I keep agents on least privilege and they can&#x27;t change their own permissions.”</span></div>
