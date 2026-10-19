# Quant-Stroller（个人项目：反过拟合的研究平台）

**Outside work I built a research platform where no strategy goes live until it passes two independent gates, and I log every idea I tried, not just the ones that worked.**

## 适用 LP

- 主：**Think Big**、**Invent and Simplify**、**Learn and Be Curious**、**Are Right, A Lot**、**Insist on the Highest Standards**
- 副：Dive Deep、Ownership、Deliver Results
- 这是**个人项目，不是雇主工作**：作 Think Big / Learn / Invent 的**补充**，不要让它成为唯一的 Think Big 答案

## 数字

- 2026-06 至今；Python **66K+ 行**、**470+ 测试文件**；覆盖美股、加密、A 股、外汇
- 窄 seam：`DataSource / Factor / Strategy / Broker`：新市场/新数据商 = 薄适配器，策略代码零改动
- 双关卡：purged 交叉验证、Deflated Sharpe Ratio、PBO + NautilusTrader 执行重放
- **340+** 次实验记入 append-only ledger；每市场校准过的交易成本模型
- 中国小盘月度策略两关均过，**excess Sharpe 1.39**（扣 **10 bps** 成本）；上线 paper-trading（Alpaca / CCXT 路由、事前风控、5 因子风险报告）
- point-in-time 数据平面（raw → bars → panel，DuckDB/Parquet）；**2,300+** 因子、**9** 个数据商；**5,500** 只 A 股面板；**8-GPU** PyTorch 训练 + 自托管 CI；FastAPI + React 研究控制台
- 【待补：340 个实验里通过双关卡的有几个（"拒绝了多少自己的想法"）——Are Right A Lot 的核心数字】

## S / T / A / R / L

### S
- 个人项目，2026-06 至今：**多市场**量化研究平台，**Python**
- 约 **66K 行**、**470+ 测试文件**；美股、加密、A 股、外汇

### T
- 设计目标：新市场或数据商 = **薄适配器**，**策略代码零改动**
- 第二个目标：**抵抗过拟合**的纪律

### A
- 保持 **4 个窄 seam**：数据源、因子、策略、broker
- 建**双关卡**：**purged CV、Deflated Sharpe、PBO**，然后 **NautilusTrader 执行重放**
- **340+** 次实验记入 **append-only ledger**，每市场有成本模型
- 把一个中国小盘月度策略过了**两个关卡**
- 部署到**实盘模拟（paper-trading）**，带**事前风控**

### R
- 扣 **10 bps** 后 **excess Sharpe 1.39**；是 paper-trading，不是盈利证明

### L
- 用**流程**反驳自己的想法：ledger 显示我试了多少
- 没有通过**两个独立关卡**，什么都不上线

## 追问与回答

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

## 换个 LP 讲

- **Think Big**：一个平台把新市场当薄适配器接入；四市场、四 seam、2,300+ 因子；说是个人研究项目，别夸成「产品」
- **Invent and Simplify**：四个窄 seam，新数据商是适配器不是重写；账本
- **Learn and Be Curious**：因为不信自己的回测，从零学 purged CV、Deflated Sharpe、PBO，并落到流水线
- **Are Right, A Lot**：建流程反驳自己的策略想法；双关卡 + 账本；340+ 实验；别把 Sharpe 1.39 当盈利证明
- **Insist on the Highest Standards**：没过两个独立关卡不上线；事前风控、成本模型

## 待补

- 【待补：340 个实验里通过双关卡的有几个】
- 【待补：为什么做这个项目，一句话动机；起点是什么问题】
- 【待补：一个架构取舍和被否决的替代方案，比如 Broker 做成 seam，或 append-only ledger 而非可覆盖的实验表】
- 【待补：一个你喜欢的想法被 DSR/PBO 拒绝的具体例子，你怎么处理】
- 【待补：学习路径（purged CV / DSR / PBO 怎么学的）】
- 【待补：用你自己的话解释 purging/embargo、DSR 修正什么】
- 【待补：paper-trading 运行多久、偏差多少】
- 【待补：point-in-time 数据平面的一个真实坑】
- 【待补：为什么选 Python / DuckDB；测试策略取舍；能否扩展到团队】
- 【待补：有没有别人用过它或从中受益（研究控制台）】
- 【待补：What I'd do differently】

<details><summary>逐字稿</summary>

> Outside work I built a multi-market quantitative research platform in Python — about sixty-six thousand lines and over four hundred and seventy test files — covering US equities, crypto, China A-shares and FX. The design goal was that adding a market or a data vendor should be a thin adapter with zero strategy-code changes, so I kept four narrow seams: data source, factor, strategy, broker.
>
> The part I'm most proud of is the discipline against overfitting. Every strategy has to pass a dual gate: purged cross-validation with Deflated Sharpe Ratio and probability of backtest overfitting, and then an execution replay on NautilusTrader. I've logged over three hundred and forty experiments to an append-only ledger with per-market cost models, so I can see how many ideas I tried, not only the ones that worked. One China small-cap monthly strategy cleared both gates with an excess Sharpe of 1.39 after ten basis points of costs, and now runs on a live paper-trading loop with pre-trade risk checks.

</details>
