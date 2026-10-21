---
id: nr-amz-g2-senior-4
node: amazon.followups
type: qa
step: 85
---
## Q
<p class="title">不依赖 agent 自述的正确性<span class="meta">03 senior 追问</span></p>

*"What did the hard cap of three agents cost you, and when would you lift it?"*

## A
<span class="label">面试官在探</span> 面试官在探：你对取舍的两面都清楚，且知道何时调整。

<span class="label">回答框架</span>

- 先说代价：并行度降低，整体速度变慢
- 再说收益：我每次返回都能复核，质量可审计，不会堆积未审的产出
- 最后说放开条件：当验收自动化到不需要我读就能放行大部分内容时，上限可以提高

<span class="label">为什么这是最佳实践</span>

并发上限的本质是人的复核带宽。瓶颈在审查而不在生成，所以只有当审查能力被自动化放大，才有理由提高上限。

<div class="sources"><b>表达 · business English</b><br>• <b><i>review bandwidth</i></b> — 审查带宽<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The cap reflects my review bandwidth, not the agents&#x27; speed.”</span><br>• <b><i>bottleneck</i></b> — 瓶颈<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The bottleneck is review, not generation.”</span></div>
