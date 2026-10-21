---
id: nr-amz-s10-senior-3
node: amazon.followups
type: qa
step: 49
---
## Q
<p class="title">退款费 billing-terms 复盘<span class="meta">03 senior 追问</span></p>

*"Why is fixing it at fee-creation time better than patching the data after the fact?"*

## A
<span class="label">面试官在探</span> 面试官在探：你对修“症状”和修“机制”的区分。

<span class="label">回答框架</span>

- 回填只能修已有的坏行，不阻止新的坏行产生
- 根因是复制了历史计划 ID，应在费用创建时解析生效计划
- 这样同时消除上游计划写入滞后带来的风险
- 回填仍然需要做，但作为一次性的清理，而不是长期方案

<span class="label">为什么这是最佳实践</span>

只做数据修补，相当于每次都在清理下游；在创建时解析生效计划，是让错误无法产生。两个脆弱点（复制历史 ID、上游滞后）的共同点是“用了过期的计划”，所以一个动作能同时覆盖。回填是治已发生的，创建时解析是防未发生的，两者缺一不可。

<div class="sources"><b>表达 · business English</b><br>• <b><i>fix the mechanism, not the symptom</i></b> — 修机制而不是症状<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I wanted to fix the mechanism, not just the symptom.”</span><br>• <b><i>make the failure impossible</i></b> — 让错误无法发生<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Resolving at fee creation makes this failure impossible.”</span></div>
