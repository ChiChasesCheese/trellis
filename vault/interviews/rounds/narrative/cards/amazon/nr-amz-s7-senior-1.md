---
id: nr-amz-s7-senior-1
node: amazon.followups
type: qa
step: 32
---
## Q
<p class="title">schema pool<span class="meta">03 senior 追问</span></p>

*"How would you measure whether the schema pool actually improved developer productivity?"*

## A
<span class="label">面试官在探</span> 面试官在探：你能否把“感觉更好”变成可度量的结果。

<span class="label">回答框架</span>

- 先选指标：DDL 冲突次数、集成测试排队时间、因共享 schema 重跑的次数
- 取得基线：用工具之前的几周数据对比
- 同时看反向指标：同步失败率、槽位泄漏、克隆耗时
- 说明现状：目前缺少团队级采用数据，我下一步先补埋点

<span class="label">为什么这是最佳实践</span>

工具价值要用前后对比来证明，只说“好用”不够。我诚实的位置是：它让我能并行跑多个会话，但没有团队级采用数据，所以下一步是先加最小埋点，再谈推广。反向指标同样重要，防止我自己看不见的维护成本。

<div class="sources"><b>表达 · business English</b><br>• <b><i>baseline</i></b> — 基线，改动前的参照数据<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I need a baseline of DDL collisions per week before claiming an improvement.”</span><br>• <b><i>adoption metric</i></b> — 采用度指标<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I don&#x27;t have a team-level adoption metric yet, so that&#x27;s the first thing I&#x27;d add.”</span></div>
