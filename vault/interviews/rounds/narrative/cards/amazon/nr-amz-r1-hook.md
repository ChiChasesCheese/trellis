---
id: nr-amz-r1-hook
node: amazon.outline
type: qa
step: 37
---
## Q
<p class="title">Quant-Stroller 研究平台<span class="meta">02 提纲</span></p>

开场第一句是什么？适用哪些 LP？要报哪些数字？

## A
<span class="label">开场</span>

**Outside work I built a research platform where no strategy goes live until it passes two independent gates, and I log every idea I tried, not just the ones that worked.**

<span class="label">适用 LP</span>

- 主：**Think Big**、**Invent and Simplify**、**Learn and Be Curious**、**Are Right, A Lot**、**Insist on the Highest Standards**
- 副：Dive Deep、Ownership、Deliver Results
- 这是**个人项目，不是雇主工作**：作 Think Big / Learn / Invent 的**补充**，不要让它成为唯一的 Think Big 答案

<span class="label">数字</span>

- 2026-06 至今；Python **66K+ 行**、**470+ 测试文件**；覆盖美股、加密、A 股、外汇
- 窄 seam：`DataSource / Factor / Strategy / Broker`：新市场/新数据商 = 薄适配器，策略代码零改动
- 双关卡：purged 交叉验证、Deflated Sharpe Ratio、PBO + NautilusTrader 执行重放
- **340+** 次实验记入 append-only ledger；每市场校准过的交易成本模型
- 中国小盘月度策略两关均过，**excess Sharpe 1.39**（扣 **10 bps** 成本）；上线 paper-trading（Alpaca / CCXT 路由、事前风控、5 因子风险报告）
- point-in-time 数据平面（raw → bars → panel，DuckDB/Parquet）；**2,300+** 因子、**9** 个数据商；**5,500** 只 A 股面板；**8-GPU** PyTorch 训练 + 自托管 CI；FastAPI + React 研究控制台
- 【待补：340 个实验里通过双关卡的有几个（"拒绝了多少自己的想法"）——Are Right A Lot 的核心数字】

<div class="sources"><b>表达 · business English</b><br>• <b><i>narrow seam</i></b> — 窄接口 / 窄的分层边界<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I kept four narrow seams so a new market never touches strategy code.”</span><br>• <b><i>append-only ledger</i></b> — 只追加不覆盖的账本<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Every experiment goes into an append-only ledger, so I can&#x27;t quietly forget the failures.”</span><br>• <b><i>net of costs</i></b> — 扣除成本之后<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The excess Sharpe of 1.39 is net of ten basis points of costs.”</span></div>
