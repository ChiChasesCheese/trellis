---
id: nr-amz-r1-senior-3
node: amazon.followups
type: qa
step: 64
---
## Q
<p class="title">Quant-Stroller 研究平台<span class="meta">03 senior 追问</span></p>

*"Why did you make append-only the rule for the experiment ledger rather than a mutable table?"*

## A
<span class="label">面试官在探</span> 面试官在探：你对数据完整性和事后可审计性的设计判断

<span class="label">回答框架</span>

- 先说问题：可覆盖的表会让失败的试验消失，过拟合的代价就看不见
- 再说取舍：追加式多占一点存储、查询稍麻烦，但换来完整历史
- 说明它如何支撑 Deflated Sharpe：试验次数必须是真实的
- 收尾：可审计性让别人也能复核结论

<span class="label">为什么这是最佳实践</span>

如果能覆盖，人就会在无意间删掉不好看的记录，试验次数被低估，统计修正就失效。追加式用一点存储成本换来诚实的分母，这是用机制而不是自律来防止自欺。

<div class="sources"><b>表达 · business English</b><br>• <b><i>audit trail</i></b> — 可审计的历史轨迹<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The append-only ledger gives me an audit trail of every idea I tried.”</span><br>• <b><i>enforce by design</i></b> — 靠设计强制保证，而不靠自觉<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I enforce honesty by design: you can&#x27;t edit a past experiment.”</span></div>
