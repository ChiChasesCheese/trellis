---
id: mlp-deepdive-pitch-quant
node: deepdive.pitch
type: qa
step: 1
---
## Q
**怎么讲 Quant-Stroller**｜项目深挖

“Pick a project you're proud of and walk me through it.”

## A
首选这个项目：它是你自己从头做的，每个决定都是你的，而且和对冲基金的工作最近。回测（backtesting）就是用历史数据检验一个交易策略；项目的立意是让人很难骗过自己。

- **60 秒版的顺序：** 一句话立意；三层架构；你做的那个决定（双重闸门）；一个结果。
- **三层：** 一是 point-in-time 数据面（只用当时已知的信息，避免前视偏差），原始文件到 K 线到面板（panel），放在 DuckDB 和 Parquet 上，约 2,300 个因子、来自 9 个数据商；二是接缝很窄的策略层，DataSource、Factor、Strategy、Broker 四个接口，新市场或新数据商只是一层薄适配；三是双重验证闸门。
- **结果：** 一个中国小盘股月度策略过了两道闸门，扣除 10 个基点成本后超额夏普约 1.39，在带事前风控和五因子风险报告的纸面交易回路里运行。
- **5 分钟版：** 在 60 秒基础上依次展开目的与用户、技术栈、数据面、最难的问题、验证、重做会改什么。

**英文答法。**
- Quant-Stroller is a **multi-market research and backtesting platform** I built this year: US equities, crypto, China A-shares and FX. Its point is to make it **hard to fool yourself** with a backtest.
- Three layers: a **point-in-time data plane** on DuckDB and Parquet; a strategy layer with **narrow seams** — DataSource, Factor, Strategy, Broker — so a new market is a thin adapter; and a **dual validation gate**.
- The decision I'd defend is the gate: **purged cross-validation, deflated Sharpe and PBO**, then an execution replay on **NautilusTrader**, before anything touches paper trading.
- One China small-cap monthly strategy passed both: **excess Sharpe about 1.39** net of 10 basis points.

**5 分钟展开。**
- **0:00 立意与用户：** make it hard to fool yourself; the user is me and future strategy researchers.
- **1:00 数据面与接缝：** raw to bars to panel; why the data plane came first.
- **2:30 验证闸门：** statistical gate, then execution gate; 340-plus experiments in an append-only ledger.
- **4:00 规模与证明：** 66K-plus lines, 470-plus test files, 5,500-stock A-share panels, PyTorch on an 8-GPU server.
- **4:45 诚实边界：** paper trading, not real money.

**追问。**
- **Is it real money?** No, paper trading with pre-trade risk checks.
- **Why "66K lines"?** It includes tests.
