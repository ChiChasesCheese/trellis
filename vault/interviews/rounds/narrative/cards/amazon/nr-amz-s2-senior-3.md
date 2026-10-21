---
id: nr-amz-s2-senior-3
node: amazon.followups
type: qa
step: 9
---
## Q
<p class="title">Quality-check 框架<span class="meta">03 senior 追问</span></p>

*"What are the risks of dynamic SQL in a framework other teams plug into, and how do you control them?"*

## A
<span class="label">面试官在探</span> 面试官在探：你是否认识到平台的风险面，并有现实的缓解措施。

<span class="label">回答框架</span>

- 先说威胁模型：配置经 migration 受控，不是用户输入，所以注入不是主要风险
- 再说真风险：失去静态检查，配置写错要到运行时才知道
- 再说缓解：exception handler 把崩溃变成 FAIL 行，结果表加健康检查
- 最后说治理：谁能改配置、怎么评审，要像改代码一样严格

<span class="label">为什么这是最佳实践</span>

判断风险要先定威胁模型，否则会把力气花在不存在的威胁上。动态 SQL 的真代价是错误延后到运行时，所以要用异常处理和对结果表本身的监控把错误尽快暴露。配置进了 migration，改动就有评审和记录。

<div class="sources"><b>表达 · business English</b><br>• <b><i>threat model</i></b> — 威胁模型<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Config goes through migrations, so in my threat model injection is not the main risk.”</span><br>• <b><i>guardrail</i></b> — 护栏<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The exception handler is a guardrail so one bad config row can&#x27;t take down other checks.”</span></div>
