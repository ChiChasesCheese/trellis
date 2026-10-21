---
id: nr-amz-s8-senior-1
node: amazon.followups
type: qa
step: 37
---
## Q
<p class="title">Terraform 7 分钟 RCA<span class="meta">03 senior 追问</span></p>

*"How would you prevent this entire class of failure instead of fixing resources one at a time?"*

## A
<span class="label">面试官在探</span> 面试官在探：你能否把一次事故变成系统性的预防机制。

<span class="label">回答框架</span>

- 先说检测前移：在 plan 阶段用 policy-as-code 或 lint 检查 ownership 资源是否设置了 outbound_privileges
- 把它接进 CI，让缺参数的 PR 无法合入
- 给模块加默认值或封装，让正确做法成为默认
- 说明现状：这个检查尚未落地，我会提议并推动

<span class="label">为什么这是最佳实践</span>

逐个修只能赶上已知的情况，机制才能挡住未来的。越早发现越便宜：plan 阶段的检查比 QA 发布失败便宜得多。我要诚实说明目前只是标出了风险，检查还没落地，下一步是把它写成 CI 规则。

<div class="sources"><b>表达 · business English</b><br>• <b><i>policy as code</i></b> — 把规则写成可执行代码<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I&#x27;d encode the rule as policy as code and run it at plan time.”</span><br>• <b><i>make the right thing the default</i></b> — 让正确做法成为默认<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Wrapping the resource in a module would make the right thing the default.”</span></div>
