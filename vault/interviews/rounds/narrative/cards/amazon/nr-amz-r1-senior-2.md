---
id: nr-amz-r1-senior-2
node: amazon.followups
type: qa
step: 63
---
## Q
<p class="title">Quant-Stroller 研究平台<span class="meta">03 senior 追问</span></p>

*"If paper-trading results drift away from the backtest, how would you decide whether to stop the strategy?"*

## A
<span class="label">面试官在探</span> 面试官在探：你有没有预先设定的停止规则，而不是事后凭感觉

<span class="label">回答框架</span>

- 事先定义可观测的偏差指标，例如成交价与回测假设的滑点差、实际成本对比 10 bps 假设
- 把偏差拆开：是成本模型偏了、数据延迟，还是策略本身失效
- 设阈值和动作：超过阈值就降仓或暂停，而不是等亏损来说服自己
- 复盘后更新成本模型或把想法写回账本

<span class="label">为什么这是最佳实践</span>

上线前就写好停止规则，是为了避免人在亏损时找借口。把偏差拆成成本、执行、信号三类，才知道该修模型还是淘汰策略；结果回写账本，下一轮实验才有真实的成本基准。

<div class="sources"><b>表达 · business English</b><br>• <b><i>kill criteria</i></b> — 预先约定的终止条件<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I would write kill criteria before the strategy goes live, not after.”</span><br>• <b><i>attribute the drift</i></b> — 把偏差归因到具体来源<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“First I would attribute the drift to costs, execution or signal.”</span></div>
