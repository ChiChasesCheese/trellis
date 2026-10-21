---
id: nr-amz-r1-followups
node: amazon.followups
type: qa
step: 61
---
## Q
<p class="title">Quant-Stroller 研究平台<span class="meta">03 追问</span></p>

面试官会追问什么？每个怎么答？

## A
- **Why a purged CV?**
    - 见待补；这是 Dive Deep 现场检验，必须是你真懂的版本
- **What does DSR correct for?**
    - 多重检验 / 非正态；用 340+ 实验作例子（细节见待补）
- **How much of the 1.39 survives costs and live?**
    - 已**扣 10 bps** 成本；只在 **paper-trading**；运行多久、偏差多少见待补
- **Biggest bug in the data plane?**
    - 见待补
- **Why Python / DuckDB?**
    - 见待补
- **How do you test a 66K-line codebase solo?**
    - **470+ 测试文件** + **自托管 CI**；测试策略取舍见待补
- **Would this scale to a team?**
    - 见待补

<div class="sources"><b>表达 · business English</b><br>• <b><i>multiple-testing penalty</i></b> — 多重检验带来的惩罚 / 修正<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“With three hundred and forty experiments, the Deflated Sharpe applies a multiple-testing penalty to the best one.”</span><br>• <b><i>leakage</i></b> — 信息泄漏（训练集看到了测试期信息）<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Purging removes the overlap between train and test labels, which is where leakage hides.”</span><br>• <b><i>bus factor</i></b> — 关键人风险（只有一个人懂）<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Being solo, the bus factor is one, so I leaned on tests and CI.”</span></div>
