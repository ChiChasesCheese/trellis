---
id: nr-amz-r2-senior-4
node: amazon.followups
type: qa
step: 70
---
## Q
<p class="title">AI-native 迁移<span class="meta">03 senior 追问</span></p>

*"How would you make this workflow safe for a whole team to adopt, not just for you?"*

## A
<span class="label">面试官在探</span> 面试官在探：你能否把个人习惯变成团队可复用的机制

<span class="label">回答框架</span>

- 先写下规则：规划、TDD、CI 和监控 gate 的流程成文
- 再放进工具链：gate 做成强制检查，而不是靠自觉
- 然后设定人工审查的范围：哪些路径必须逐 diff 读，比如资金相关
- 最后收集反馈：定期复盘 agent 出错的案例并更新规则

<span class="label">为什么这是最佳实践</span>

个人纪律无法规模化，机制可以。把 gate 放进 CI，团队里每个人即使经验不同也会走同一道校验；明确哪些代码必须人读，限定 agent 的爆炸半径。这是我下一步会推进的做法，目前团队里已被采用的是 schema pool 与 on-call copilot。

<div class="sources"><b>表达 · business English</b><br>• <b><i>blast radius</i></b> — 出错时的影响范围<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Requiring human review on money paths keeps the blast radius of agent mistakes small.”</span><br>• <b><i>guardrails</i></b> — 护栏，防止出错的强制约束<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I&#x27;d encode the rules as CI guardrails so nobody has to remember them.”</span></div>
