---
id: mlp-finance-dt-backtest
node: finance.data
step: 2
type: qa
---
## Q
**回测与它的常见偏差**｜金融常识

"什么是回测（backtest）？有哪些常见陷阱？数据工程师能做什么？"

## A
**回测** 是用历史数据模拟一个策略，估计它如果当时运行会赚多少。它是策略研究的核心工具。

**常见陷阱。**
- **前视偏差：** 用到了当时还不知道的数据，比如用当天收盘后才发布的数据去决定当天开盘的交易。
- **幸存者偏差（survivorship bias）：** 股票池里只有今天还活着的股票，退市和破产的被漏掉，收益被高估；解法是用历史成分股，即每个时点真实存在的股票池。
- **过拟合（overfitting）：** 试了很多参数和策略，挑出恰好在历史上表现好的那个，它的好表现多半只是运气。检验方法包括清洗交叉验证（purged cross-validation，去掉测试集前后重叠的样本，避免训练集信息泄露到测试集）和回测过拟合概率（PBO）。
- **忽略成本：** 没扣佣金、价差和冲击成本，实盘表现会差很多。

**对数据工程师意味着什么。**
- **数据面决定可信度：** 回测用的数据是原始、行情、面板这样分层加工的；每一层都要按时点保证只用当时已有的信息。
- **要有完整历史：** 保留退市标的和历史成分，才能避免幸存者偏差。
- **可复现：** 同样的输入必须跑出同样的结果，方便核对。

**英文答法。**
- "A **backtest** simulates a strategy on historical data, and its main risks are look-ahead bias and overfitting."
- "To avoid **survivorship bias** I'd keep delisted names and historical constituents."
