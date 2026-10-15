# R1 · Quant-Stroller（个人项目：反过拟合的研究平台）

> 来源：**仅简历**（`core/resume/resume.tex`，Projects，Jun 2026–Present）。没有 `core/stories/` 笔记 → 下面只用简历里的事实，其余全部 `【待 Chi 补】`。
> 这是**个人项目，不是雇主工作**：LP 面试里作为 Think Big / Learn and Be Curious / Invent and Simplify 的**补充**，不要让它成为唯一的 Think Big 答案（见 `../story_matrix.md` 的 sole-primary 风险）。
> 主 LP：**Think Big · Invent and Simplify · Learn and Be Curious · Are Right, A Lot · Insist on the Highest Standards**；副：Dive Deep · Ownership · Deliver Results。

## 1. 数字（简历原文）

| 事实 | 简历表述 |
|---|---|
| 规模 | Python，66K+ 行，470+ 测试文件；覆盖美股、加密、A 股、外汇 |
| 抽象 | 窄 `DataSource / Factor / Strategy / Broker` seam：接入新市场/新数据商 = 薄适配器，策略代码零改动 |
| 反过拟合 | 双关卡（dual-gate）：purged 交叉验证、Deflated Sharpe Ratio、PBO + NautilusTrader 执行重放 |
| 实验账本 | 340+ 次实验记入 append-only ledger；每市场校准过的交易成本模型 |
| 验证过的策略 | 中国小盘月度策略，两关均通过，**excess Sharpe 1.39（扣 10 bps 成本）**；上线 paper-trading（Alpaca / CCXT 路由、事前风控、5 因子风险报告） |
| 数据 | point-in-time 数据平面（raw → bars → panel，DuckDB/Parquet）；2,300+ 因子目录、9 个数据商；5,500 只 A 股面板；8-GPU 服务器 PyTorch 训练 + 自托管 CI；FastAPI + React 研究控制台 |

## 2. 60–90 秒（口述提纲）

**"Outside work I built a research platform where no strategy goes live until it passes two independent gates, and I log every idea I tried, not just the ones that worked."**

**S · Situation**
- Personal project, **Jun 2026–present**: a **multi-market** quant research platform in **Python**.
- About **66K lines**, **470+ test files**; US equities, crypto, China A-shares, FX.

**T · Task**
- Design goal: a new market or vendor is a **thin adapter**, **zero strategy-code changes**.
- Second goal: **discipline against overfitting**.

**A · Action** (in the order the resume lists it)
1. Kept **four narrow seams**: data source, factor, strategy, broker.
2. Built a **dual gate**: **purged cross-validation, Deflated Sharpe, PBO**, then **NautilusTrader execution replay**.
3. Logged **340+ experiments** to an **append-only ledger**, with per-market cost models.
4. Ran a China small-cap monthly strategy through **both gates**.
5. Deployed it to a **live paper-trading loop** with **pre-trade risk checks**.

**R · Result**
- **Excess Sharpe 1.39** after **10 bps** costs; paper-trading, not proof of profit.
- 【待 Chi 补：340 个实验里通过双关卡的有几个（"拒绝了多少自己的想法"）——这是 Are Right A Lot 的核心数字】

**L · Learning / Mechanism**
- A **process to disconfirm my own ideas**: the ledger shows how many I tried.
- Nothing goes live without passing **two independent gates**.

<details><summary>逐字稿（参考，不背）</summary>

> Outside work I built a multi-market quantitative research platform in Python — about sixty-six thousand lines and over four hundred and seventy test files — covering US equities, crypto, China A-shares and FX. The design goal was that adding a market or a data vendor should be a thin adapter with zero strategy-code changes, so I kept four narrow seams: data source, factor, strategy, broker.
>
> The part I'm most proud of is the discipline against overfitting. Every strategy has to pass a dual gate: purged cross-validation with Deflated Sharpe Ratio and probability of backtest overfitting, and then an execution replay on NautilusTrader. I've logged over three hundred and forty experiments to an append-only ledger with per-market cost models, so I can see how many ideas I tried, not only the ones that worked. One China small-cap monthly strategy cleared both gates with an excess Sharpe of 1.39 after ten basis points of costs, and now runs on a live paper-trading loop with pre-trade risk checks.
>
> 【待 Chi 补：340 个实验里通过双关卡的有几个（"拒绝了多少自己的想法"）——这是 Are Right A Lot 的核心数字】

</details>

## 3. 2 分钟（口述提纲）

在 §2 基础上补三段（每段都有待补，不要用推测填）。

**"Outside work I built a research platform where no strategy goes live until it passes two independent gates, and I log every idea I tried, not just the ones that worked."**

**S · Situation**
- Personal project, **Jun 2026–present**; **Python**, **66K+ lines**, **470+ test files**, four markets.
- Why I started: 【待 Chi 补：为什么做这个项目，一句话动机；起点是什么问题（例如被过拟合坑过一次？）】

**T · Task**
- Make a new market or vendor a **thin adapter** with **zero strategy-code changes**.
- Make **overfitting** hard to hide.

**A · Action** (in the order the resume lists it)
1. **Four narrow seams**: data source, factor, strategy, broker.
2. A decision with a rejected alternative: 【待 Chi 补：一个架构取舍——例如"把 Broker 做成 seam 而不是在策略里直接调交易所 API"，你否决了什么；或"只存 append-only ledger 而不是可覆盖的实验表"，原因】
3. **Dual gate**: **purged CV, DSR, PBO**, then **NautilusTrader** execution replay.
4. **Append-only ledger**: **340+ experiments**, calibrated per-market **cost models**.
5. A time the gate said no: 【待 Chi 补：一个你喜欢的想法被 DSR/PBO 拒绝的具体例子，你如何处理（Are Right A Lot：disconfirm 自己）】
6. Validated a **China small-cap monthly** strategy through both gates.
7. Deployed to **paper trading**: **Alpaca/CCXT** routing, **pre-trade risk checks**, **5-factor risk report**.
8. Also built the **point-in-time data plane** (raw to bars to panel, **DuckDB/Parquet**), **2,300+ factors** across **9 vendors**.

**R · Result**
- **Excess Sharpe 1.39** net of **10 bps**; live in **paper trading**, so not a profit claim.
- 5,500-stock A-share panels, **8-GPU** PyTorch training, **self-hosted CI**, **FastAPI + React** console.
- Gate pass count: 【待 Chi 补：340 个实验里通过双关卡的有几个】

**L · Learning / Mechanism**
- **Disconfirm my own ideas** with a process, not willpower.
- What I'd do differently: 【待 Chi 补】

## 4. 适用 LP 与改角度

| LP | 开场一句 | 重点讲 | 避免 |
|---|---|---|---|
| **Think Big** (P) | "I wanted one platform that onboards a new market as a thin adapter." | 四市场、四 seam、2,300+ 因子 | 夸成"产品"；说是个人研究项目 |
| **Invent and Simplify** (P) | "Four narrow seams so a new vendor is an adapter, not a rewrite." | seam 设计；账本 | — |
| **Learn and Be Curious** (P) | "I taught myself purged CV, Deflated Sharpe and PBO because I didn't trust my own backtests." | 从零学统计检验并落到流水线 | 【待 Chi 补：学习路径】 |
| **Are Right, A Lot** (P) | "I built a process to disconfirm my own strategy ideas." | 双关卡 + 账本；340+ 实验 | 把 Sharpe 1.39 当"盈利证明"——只是 paper-trading |
| **Insist on the Highest Standards** (P) | "Nothing goes live without passing two independent gates." | 事前风控、成本模型 | — |

## 5. 追问（≥5）

1. **Why a purged CV?**
   - 【待 Chi 补：用你自己的话解释 purging/embargo 的理由；这是 Dive Deep 现场检验，必须是你真的懂的版本】
2. **What does DSR correct for?**
   - 【待 Chi 补】（多重检验 / 非正态；用 340+ 实验作为例子）
3. **How much of the 1.39 survives costs and live?**
   - Resume: **net of 10 bps** costs; **paper-trading** only.
   - 【待 Chi 补：paper-trading 运行多久、偏差多少】
4. **Biggest bug in the data plane?**
   - 【待 Chi 补：point-in-time 的一个真实坑】
5. **Why Python / DuckDB?**
   - 【待 Chi 补】
6. **How do you test a 66K-line codebase solo?**
   - **470+ test files** and **self-hosted CI** (resume).
   - 【待 Chi 补：测试策略取舍】
7. **Would this scale to a team?**
   - 【待 Chi 补】

## 6. Senior 升级点（bar = senior）

当前档位：**scope 与 rigor 是 senior 级，但无 influence/cross-team**（个人项目）。
- 【待 Chi 补：有没有别人用过它/从中受益（朋友、同事用研究控制台？）】
- 只用于 Think Big / Learn / Are Right 的补充；**employer 工作里的 Think Big 缺口**见 `../story_matrix.md`。
