---
id: nr-amz-r1-senior-1
node: amazon.followups
type: qa
step: 62
---
## Q
<p class="title">Quant-Stroller 研究平台<span class="meta">03 senior 追问</span></p>

*"How would you know a strategy that passed both gates is not just a lucky survivor of 340 experiments?"*

## A
<span class="label">面试官在探</span> 面试官在探：你是否真正理解多重检验，以及通过关卡不等于真的有效

<span class="label">回答框架</span>

- 先承认：试得越多，最好的那个越可能只是运气，所以 Deflated Sharpe 要按试验次数惩罚
- 再说账本的作用：试验总数是分母，必须诚实记录，否则修正没有意义
- 然后说外部证据：样本外和 paper-trading 的表现是否和回测一致
- 最后说态度：把 1.39 当作假设而不是盈利证明，持续监控偏差

<span class="label">为什么这是最佳实践</span>

最大的统计陷阱是只看赢家。账本把所有试验都记下来，Deflated Sharpe 才能按真实的试验次数扣掉运气成分；再用 paper-trading 这种从未参与调参的数据做最终检验。这样结论的可信度来自流程，而不是某个漂亮的数字。

<div class="sources"><b>表达 · business English</b><br>• <b><i>survivorship in your own research</i></b> — 自己研究过程中的幸存者偏差<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The ledger protects me from survivorship in my own research.”</span><br>• <b><i>out-of-sample evidence</i></b> — 样本外证据<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Paper trading is the out-of-sample evidence the backtest could never give me.”</span></div>
