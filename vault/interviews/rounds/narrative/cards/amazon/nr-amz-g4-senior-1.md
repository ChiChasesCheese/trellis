---
id: nr-amz-g4-senior-1
node: amazon.followups
type: qa
step: 92
---
## Q
<p class="title">什么时候信任 LLM<span class="meta">03 senior 追问</span></p>

*"How would you build an oracle for a task that currently has none?"*

## A
<span class="label">面试官在探</span> 面试官在探：你遇到没有验证手段的问题时，会不会主动造验证手段。

<span class="label">回答框架</span>

- 先问能否把问题拆出一个可验证的子问题，比如把数字变成可复算的脚本
- 再找独立路径：用另一种方法得到同一个答案做对拍
- 实在造不出来，就把任务降级为草稿，由我重写，或者交给人做

<span class="label">为什么这是最佳实践</span>

没有 oracle 并不意味着只能盲信或放弃，往往可以造一个。造 oracle 的成本通常小于出错的代价，而且造好之后对未来的模型也有效。造不出来就诚实降级，比假装可信更稳妥。

<div class="sources"><b>表达 · business English</b><br>• <b><i>independent path</i></b> — 独立验证路径<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I look for an independent path that reaches the same answer.”</span><br>• <b><i>downgrade to a draft</i></b> — 降级为草稿<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Without an oracle, I downgrade the output to a draft and rewrite it.”</span></div>
