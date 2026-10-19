---
id: nr-amz-g4-senior-2
node: amazon.followups
type: qa
step: 93
---
## Q
<p class="title">什么时候信任 LLM<span class="meta">03 senior 追问</span></p>

*"What if the oracle itself is wrong, for example tests written by the same agent that wrote the code?"*

## A
<span class="label">面试官在探</span> 面试官在探：你是否看到 oracle 的同源盲区。

<span class="label">回答框架</span>

- 先承认：测试和代码同源时会共享盲区，全绿不证明正确
- 再说对策：变异测试看测试能否抓住故意写错的版本
- 最后说独立路径对拍，以及关键部分由人写或人审测试

<span class="label">为什么这是最佳实践</span>

oracle 也需要被检验。让测试和代码来自不同来源，或者用变异测试和独立实现对拍，才能打破同源盲区。这是我规则的已知失效点，主动说出来更可信。

<div class="sources"><b>表达 · business English</b><br>• <b><i>common-mode failure</i></b> — 同源故障<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Tests from the same author as the code risk a common-mode failure.”</span><br>• <b><i>cross-check</i></b> — 交叉核对<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I cross-check with an independent implementation.”</span></div>
