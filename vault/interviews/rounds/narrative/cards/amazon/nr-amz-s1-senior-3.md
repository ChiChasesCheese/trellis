---
id: nr-amz-s1-senior-3
node: amazon.followups
type: qa
step: 4
---
## Q
<p class="title">Amex 结算管线<span class="meta">03 senior 追问</span></p>

*"What is the blast radius if this pipeline produces a wrong fee, and how do you contain it?"*

## A
<span class="label">面试官在探</span> 面试官在探：你对出错影响面的意识，以及止损手段是否事先设计好。

<span class="label">回答框架</span>

- 先说影响链：费用计算的输出会喂给出款，所以错误会变成真实的钱
- 再说止损：feature flag 一条 UPDATE 就能急停，不需要发版
- 再说留痕：不匹配进 error log，所以能知道受影响范围并更正
- 最后说事后：已经被下游消费的错误要走更正分录，而不是悄悄改回去

<span class="label">为什么这是最佳实践</span>

止损手段必须在出事之前就存在：急停要快（不依赖发版），范围要可知（error log 留痕）。下游已经消费的错误状态不能回滚，只能用更正记录补上，这样账目才有可追溯的历史。

<div class="sources"><b>表达 · business English</b><br>• <b><i>blast radius</i></b> — 爆炸半径（出错的影响范围）<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The kill switch let me shrink the blast radius to minutes, not a release cycle.”</span><br>• <b><i>correcting entry</i></b> — 更正分录<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“For fees already consumed downstream, we issue a correcting entry rather than rewriting history.”</span></div>
