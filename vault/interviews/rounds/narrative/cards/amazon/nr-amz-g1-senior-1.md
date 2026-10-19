---
id: nr-amz-g1-senior-1
node: amazon.followups
type: qa
step: 77
---
## Q
<p class="title">一个自信的错数字<span class="meta">03 senior 追问</span></p>

*"How do you know the rule actually prevents the next wrong number, rather than just feeling thorough?"*

## A
<span class="label">面试官在探</span> 面试官在探：你有没有衡量规则有效性，而不是只靠感觉。

<span class="label">回答框架</span>

- 先说可观测的信号：之后每一批题的验收里，被复算抓到的错数字数量有没有下降
- 再说对照：把规则写进指令之前和之后，同类缺陷的出现频率对比
- 最后说残余风险：规则管得住算术，管不住合理假设上的错误结论，那一类仍靠人读

<span class="label">为什么这是最佳实践</span>

规则只有在能被观察到起效时才算机制。算术类缺陷可以被机器复算抓到，所以能直接数；而假设矛盾这类缺陷机器看不见，需要明确承认它仍依赖人读。把能量化和不能量化的部分分开说，面试官更信任你的判断。

<div class="sources"><b>表达 · business English</b><br>• <b><i>leading indicator</i></b> — 先行指标<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Defects caught at the gate are a leading indicator that the rule is working.”</span><br>• <b><i>residual risk</i></b> — 残余风险<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The residual risk is a wrong conclusion built on a plausible assumption.”</span></div>
