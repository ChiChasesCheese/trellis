---
id: nr-amz-s3-senior-4
node: amazon.followups
type: qa
step: 15
---
## Q
<p class="title">ACH 费用 NULL 事故<span class="meta">03 senior 追问</span></p>

*"What would you change in the team process so that incidents like this are caught before they reach production?"*

## A
<span class="label">面试官在探</span> 面试官在探：你能否从一次事故上升到流程和组织层面的改进。

<span class="label">回答框架</span>

- 先说灰度：新路径放量前，要有该路径的完整端到端检查
- 再说评审：新增分支时检查所有共享函数是否都覆盖了它
- 再说测试策略：fixture 覆盖每种 payment type，跨 promotion 到费用生成
- 最后说传播：把 postmortem 的测试盲区变成团队的测试清单

<span class="label">为什么这是最佳实践</span>

一个事故反映的往往是流程缺口：新路径上线时没有覆盖它的端到端检查。把盲区写成清单，下次新增路径就有现成的核对项。流程改进要小而具体，才会真的被执行。

<div class="sources"><b>表达 · business English</b><br>• <b><i>pre-launch checklist</i></b> — 上线前核对清单<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I would add a pre-launch checklist item: every shared function covers the new payment type.”</span><br>• <b><i>systemic fix</i></b> — 系统性修复<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The postmortem pushed a systemic fix rather than blaming one person.”</span></div>
