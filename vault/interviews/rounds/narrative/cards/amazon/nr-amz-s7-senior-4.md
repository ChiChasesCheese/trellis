---
id: nr-amz-s7-senior-4
node: amazon.followups
type: qa
step: 35
---
## Q
<p class="title">schema pool<span class="meta">03 senior 追问</span></p>

*"You run several AI agents in parallel on one repo. How do you keep quality and safety under control?"*

## A
<span class="label">面试官在探</span> 面试官在探：你对 AI 辅助开发的工程纪律，而不是只会用工具。

<span class="label">回答框架</span>

- 先说隔离：每个会话独立槽位、独立分支，互不影响
- 再说流程：和 agent 先做计划，每个阶段先写测试，再实现
- 质量关卡：CI 与监控的阈值，钱相关代码我逐个读 diff
- 最后说边界：权限最小化，危险操作需要人确认

<span class="label">为什么这是最佳实践</span>

并行带来速度，也放大错误，所以隔离和关卡缺一不可。克隆让每个会话互不污染，TDD 和 CI 让错误尽早暴露，对钱相关代码人工读每个 diff，则把最贵的错误挡在人这一层。我看的是关卡和阈值，不是代码行数。

<div class="sources"><b>表达 · business English</b><br>• <b><i>guardrails</i></b> — 护栏，防止出错的限制<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Isolation and CI act as guardrails when several agents work in parallel.”</span><br>• <b><i>human in the loop</i></b> — 关键环节有人参与<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“For money code I keep a human in the loop and read every diff.”</span></div>
