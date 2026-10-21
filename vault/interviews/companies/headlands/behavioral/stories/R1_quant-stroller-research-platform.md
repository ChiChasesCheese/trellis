# R1 · Quant-Stroller：为了搞懂"回测有多少能活下来"而自己造的研究平台（好奇心 · 自动化与测试 · 为什么做交易）

- 用于：why trading / curiosity / a project you're proud of / how do you test。
- **先说：it's a personal project, not my employer's work.** 只讲下面列出的事实，别加性能或盈利数字。

**Hook：「I built a research platform to see how much of a good-looking backtest survives realistic costs.」**

## 数字

- Python，66K+ 行，470+ 测试文件；美股、加密、A 股、外汇。
- 340+ 次实验记入只增不改的账本（append-only ledger）。
- 一个 A 股小盘月度策略过两道门：扣除 10 bps 成本后超额 Sharpe 1.39，上了 paper trading。
- 点时数据平面（DuckDB/Parquet）；5,500 只 A 股面板；8-GPU 服务器 PyTorch + 自托管 CI。

## 60 秒

**S**
- I wanted to know how much of a **good-looking backtest** survives **realistic costs** and **out-of-sample** checks. 【待补：触发它的具体那件事】

**T**
- A platform where **adding a market or strategy** never touches **core code**, and every experiment leaves a **record**.

**A**
1. **Four narrow interfaces**: data source, factor, strategy, broker; a new market is a **thin adapter**.
2. A **point-in-time** data plane: a backtest never uses data that **wasn't yet known**.
3. A **dual gate**: **purged cross-validation**, **Deflated Sharpe**, **PBO**, then **execution replay**.
4. **Per-market cost models** and **340+ experiments** in an **append-only ledger**.
5. **470+ test files** and **self-hosted CI**, so a change can't silently alter a result.

**R**
- One **China small-cap** strategy cleared **both gates**: **1.39** excess Sharpe after **10 bps**; now on **paper trading** (not proof of profit).

**L**
- **Most ideas die at the gates**; the **ledger** shows how many I tried.

## 2 分钟（在 60 秒上加）

- **Paper-trading loop**: Alpaca/CCXT routing, **pre-trade risk checks**, a 5-factor risk report.
- **Why the gates exist**:
  - **Point-in-time**: using later-revised or future data **inflates** results.
  - **Purged CV**: labels span time, so samples near the train/test boundary **share information**; purging removes the overlap.
  - **Deflated Sharpe**: the more you try, the likelier the best is **luck**; it discounts for **number of trials**, hence the honest ledger.
  - **PBO**: the chance the in-sample winner **ranks below median** out of sample.
- **Different next time**: 【待补：下次会怎么做不同】

## 追问

- **Why four interfaces?** A new market is a **thin adapter**; strategy code **doesn't change**.
- **Why point-in-time?** Otherwise the backtest **uses information it couldn't have had**.
- **Why an append-only ledger?** Prevents recording **only the winners**. 【待补：你的具体理由】
- **Was a strategy ever blocked?** 【待补：哪道门拦下的】
- **Paper vs backtest gap?** **Fills, latency, costs, impact**. 【待补：真实偏差，或 "not enough sample yet"】
- **How would you speed up the engine?** **Profile first**, check **columnar layout**, **vectorize**, avoid per-row Python. (思路，不是我做过的事)
- **Would it scale to a firm like this?** No; the real platform is bigger in **data volume, distribution, reliability**, which is the layer I want to learn.

## 别说

- 任何延迟 / 吞吐 / 加速数字；盈利；暗示做过实盘。
- 把 paper trading 当盈利证明。

## 待补

- 【待补：触发项目的事；340 个实验过关几个；一个测试救过你的例子；paper trading 跑了多久】
