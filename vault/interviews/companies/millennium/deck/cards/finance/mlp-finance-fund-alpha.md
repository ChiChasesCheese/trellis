---
id: mlp-finance-fund-alpha
node: finance.fund
step: 3
type: qa
---
## Q
**alpha、beta、因子与夏普比率**｜金融常识

"alpha 和 beta 有什么区别？夏普比率（Sharpe ratio）衡量什么？"

## A
**beta** 是收益里跟着整个市场涨跌的那部分，买指数就能得到。**alpha** 是扣掉市场影响之后、由策略本身带来的超额收益。对冲基金卖的就是 alpha，所以它们会做空或对冲掉市场部分。

**因子（factor）** 是解释大批股票收益的共同来源，例如市场、规模、价值、动量。因子风险模型把一个组合的收益拆成"对各因子的暴露"加"个股自身的部分"，用来知道组合的风险到底来自哪里。

**信号（signal）** 是对未来相对收益的预测；评估信号，就是看它扣掉成本后在样本外还能不能预测。

**夏普比率（Sharpe ratio）** 是超额收益除以波动率（年化），即每承担一单位风险换来多少收益。同样收益，波动越小夏普越高。试过很多策略再挑最好的，夏普会被高估，所以有"降低多重测试影响的夏普"（deflated Sharpe）这类修正。

**对数据工程师意味着什么。**
- **研究要数据：** 因子和信号的计算依赖干净、时点正确的历史数据。
- **评估怕偏差：** 数据里混进未来信息，夏普会虚高；因此数据平台要保证 as-of 正确。

**英文答法。**
- "**Alpha** is return beyond the market; **beta** is the part that just follows the market."
- "**Sharpe** is excess return per unit of volatility."
