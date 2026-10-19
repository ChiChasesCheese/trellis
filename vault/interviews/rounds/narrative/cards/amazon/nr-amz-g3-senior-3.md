---
id: nr-amz-g3-senior-3
node: amazon.followups
type: qa
step: 89
---
## Q
<p class="title">GenAI 不必要的时候<span class="meta">03 senior 追问</span></p>

*"As models get cheaper and faster, does your rule about not delegating small fixes still hold?"*

## A
<span class="label">面试官在探</span> 面试官在探：你的原则是否随条件变化而更新，而不是教条。

<span class="label">回答框架</span>

- 先说规则背后的原因是成本和确定性，不是对模型的偏见
- 再说随成本下降，阈值会移动：更多小任务会变得值得委派
- 但确定性问题仍然应该用脚本，因为脚本给的是 oracle，模型给的是看起来合理的答案

<span class="label">为什么这是最佳实践</span>

好的规则要说明它依赖的前提。成本类前提会变，所以阈值要定期复核；确定性类前提不会变，所以计数永远交给脚本。区分这两类前提，说明你理解规则而不是背规则。

<div class="sources"><b>表达 · business English</b><br>• <b><i>revisit the threshold</i></b> — 重新审视阈值<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I&#x27;d revisit the threshold as costs change.”</span><br>• <b><i>first principles</i></b> — 从第一性原理出发<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I reason from first principles, not from a fixed rule.”</span></div>
