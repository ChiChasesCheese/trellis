---
id: nr-amz-g1-senior-3
node: amazon.followups
type: qa
step: 79
---
## Q
<p class="title">一个自信的错数字<span class="meta">03 senior 追问</span></p>

*"The 1,560x ratio case passed your arithmetic check. Why did it still need a new rule?"*

## A
<span class="label">面试官在探</span> 面试官在探：你是否理解检查只覆盖它设计要覆盖的那一层。

<span class="label">回答框架</span>

- 先说每一步算术都对，复算脚本只验证单个数字，验证不了数字之间的一致性
- 再说错误出在两个相互矛盾的假设上，是结构性问题而不是计算问题
- 最后说所以新增一条规则：假设之间必须互相一致，并在 review 时专门核对

<span class="label">为什么这是最佳实践</span>

单点检查通过不代表整体正确。检查的粒度决定它能发现什么：数字级检查发现不了假设级矛盾。发现盲区后补一条针对性规则，而不是假设旧检查已经够用。

<div class="sources"><b>表达 · business English</b><br>• <b><i>blind spot</i></b> — 盲区<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“A per-number check has a blind spot for contradicting assumptions.”</span><br>• <b><i>internal consistency</i></b> — 内部一致性<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I added a rule that assumptions must hold internal consistency.”</span></div>
