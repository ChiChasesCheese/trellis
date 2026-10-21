---
id: nr-amz-g4-senior-4
node: amazon.followups
type: qa
step: 95
---
## Q
<p class="title">什么时候信任 LLM<span class="meta">03 senior 追问</span></p>

*"Where would you draw the line on letting an agent act with higher autonomy, such as merging its own change?"*

## A
<span class="label">面试官在探</span> 面试官在探：你对自主性、权限与风险的判断。

<span class="label">回答框架</span>

- 先说前提：改动小、有强 oracle、可一键回滚、爆炸半径有限
- 再说仍需保留的人工点：涉及钱、安全和权限的改动必须由人批准
- 最后说渐进放权：先在低风险区域试，用数据证明可靠后再扩大

<span class="label">为什么这是最佳实践</span>

自主性应与可验证性和可回滚性成正比。高风险区域保留人工审批是对爆炸半径的管理，而不是对 AI 的不信任。渐进放权并用数据证明，比一次性开放更容易被组织接受。

<div class="sources"><b>表达 · business English</b><br>• <b><i>reversible</i></b> — 可回滚的、可撤销的<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I&#x27;d grant autonomy only for changes that are cheap and reversible.”</span><br>• <b><i>graduated autonomy</i></b> — 逐级放权<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I&#x27;d roll out graduated autonomy, starting in low-risk areas.”</span></div>
