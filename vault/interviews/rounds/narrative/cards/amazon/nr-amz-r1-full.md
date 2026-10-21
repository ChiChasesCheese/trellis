---
id: nr-amz-r1-full
node: amazon.full
type: qa
step: 13
---
## Q
<p class="title">Quant-Stroller 研究平台<span class="meta">01 完整故事</span></p>

先在心里把前因后果过一遍，再用英文完整讲一遍。

## A
<span class="label">前因后果</span>

- 背景：2026-06 起我在工作之外做了一个多市场量化研究平台，Python，约 66K 行、470+ 测试文件，覆盖美股、加密、A 股、外汇。
- 目标：新市场或新数据商只需要一个薄适配器，策略代码零改动，所以我只保留四个窄接口（数据源、因子、策略、broker）；第二个目标是抵抗过拟合，因为我不信任自己的回测。
- 我做了什么：任何策略都必须过两个独立关卡，先是 purged 交叉验证加 Deflated Sharpe 和 PBO，再是 NautilusTrader 的执行重放；340+ 次实验全部记入 append-only ledger，并按市场校准成本模型，这样能看到我试了多少想法，而不只是成功的那几个。
- 结果：一个中国小盘月度策略两关都过，扣 10 bps 成本后 excess Sharpe 1.39，并上线了带事前风控的 paper-trading；这是模拟盘，不是盈利证明。
- 为什么这样做：回测很容易自欺，所以用流程而不是直觉来反驳自己的想法，没通过两个独立关卡就不上线；账本让多重检验的代价可见。

<span class="label">英文口述（60–90 秒）</span>

Outside work, since June 2026, I built a multi-market quantitative research platform in Python, about sixty-six thousand lines and over four hundred and seventy test files, covering US equities, crypto, China A-shares and FX. The design goal was that adding a market or a data vendor should be a thin adapter with zero strategy-code changes, so I kept four narrow seams: data source, factor, strategy and broker. The part I'm most proud of is the discipline against overfitting. Every strategy has to pass a dual gate: purged cross-validation with Deflated Sharpe Ratio and probability of backtest overfitting, and then an execution replay on NautilusTrader. I've logged over three hundred and forty experiments to an append-only ledger, with per-market cost models, so I can see how many ideas I tried, not only the ones that worked. One China small-cap monthly strategy cleared both gates with an excess Sharpe of 1.39 after ten basis points of costs, and it now runs on a paper-trading loop with pre-trade risk checks. To be clear, that is paper trading, not proof of profit.

<div class="sources"><b>表达 · business English</b><br>• <b><i>thin adapter</i></b> — 很薄的适配层，只做转换、不含业务逻辑<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Adding a new data vendor is just a thin adapter, so the strategy code never changes.”</span><br>• <b><i>guard against overfitting</i></b> — 防范过拟合<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The whole platform is built to guard against overfitting my own backtests.”</span><br>• <b><i>clear a gate</i></b> — 通过一道关卡<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“One China small-cap strategy cleared both gates after costs.”</span></div>
