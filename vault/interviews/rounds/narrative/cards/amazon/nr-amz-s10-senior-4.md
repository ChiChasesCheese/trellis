---
id: nr-amz-s10-senior-4
node: amazon.followups
type: qa
step: 50
---
## Q
<p class="title">退款费 billing-terms 复盘<span class="meta">03 senior 追问</span></p>

*"How do you decide how much verification is enough for a sizing number that others will act on?"*

## A
<span class="label">面试官在探</span> 面试官在探：你如何在速度与严谨之间取舍，对决策型数字的标准是什么。

<span class="label">回答框架</span>

- 看这个数字会驱动什么动作：回填、通知商户、金额调整都不可逆或成本高
- 至少做一次抽样核对和一次独立视角的谓词复查
- 每个结论配一条可重跑的查询，读者可以自己验证
- 说明口径，比如金额口径是 SUM(ABS(amount))/100

<span class="label">为什么这是最佳实践</span>

核对的力度应与数字驱动的动作的成本成正比：只是讨论用的粗估可以快，而决定补救范围的数字必须可审计。写明口径并附上可重跑的查询，读的人才能区分“我信你”和“我验证过”，这也让纠错更便宜。

<div class="sources"><b>表达 · business English</b><br>• <b><i>auditable</i></b> — 可审计的<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Anything that drives remediation has to be auditable.”</span><br>• <b><i>proportionate rigor</i></b> — 与风险相称的严谨<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I try to apply proportionate rigor to numbers others will act on.”</span></div>
