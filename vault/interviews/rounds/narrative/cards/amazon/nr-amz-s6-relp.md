---
id: nr-amz-s6-relp
node: amazon.outline
type: qa
step: 18
---
## Q
<p class="title">费用异常检测器 go/no-go<span class="meta">02 提纲</span></p>

换成别的 LP 问时，强调哪一段？

## A
- **Are Right, A Lot**：生产前就用生产现实检验项目；强调 QA vs 生产量级、风险排序、制度化 gate；别把评估数字当已验证事实
- **Dive Deep**：问题不在模型，在 QA 永远跑不到的 numpy 循环；逐行推理 vs set-based；分布（前两个商户占 97%）
- **Have Backbone**：所有人期待我做完上线，我写下为什么不该，并冻结工作；用文档而非情绪；不是 disagree-and-commit
- **Ownership**：做的人要走了，我决定什么必须留下；先救标注
- **Frugality**：业务驱动出现前，2–3 个月重训不值得；不按沉没成本排序；无成本数字，别编
- **Invent and Simplify**：确定性规则根本不需要 ML；Phase 1 纯 SQL
- **Bias for Action**：离职前把标注导出，这是单向门

<div class="sources"><b>表达 · business English</b><br>• <b><i>say no with evidence</i></b> — 用证据说不<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I said no with a written assessment rather than with opinion.”</span><br>• <b><i>irreversible</i></b> — 不可逆的<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The analyst labels were the one irreversible loss, so exporting them was the urgent step.”</span><br>• <b><i>paged at 3 a.m.</i></b> — 凌晨三点被呼叫<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I&#x27;d rather stop a project than ship one that gets the team paged at 3 a.m.”</span></div>
