# 速记卡 · 金融词汇（LEaD 看 "interest in finance"，不考公式；能把简历上的词解释清楚即可）

> 来源：Quant-Stroller 简历条目 · Steve Johnson 官方建议（"build and back test a simple trading strategy in Python"）· QuantVault OA "multi-currency PnL"。每张一句英文定义 + 一句"我在哪用过"。

1. **Multi-manager / pod**：a firm allocates capital to many independent portfolio managers (pods), each with their own strategy and risk budget; the firm runs shared risk, infrastructure and technology. → LEaD 轮岗横跨服务 pod 的前台技术与中后台。
2. **Front / middle / back office**：front = trading & research (PMs, execution); middle = risk, P&L, compliance; back = settlement, accounting, operations. → JD 原话 "applications spanning front-office, middle-office and back-office"。
3. **Backtest**：simulate a strategy on historical data to estimate how it would have performed. → Quant-Stroller 的核心；风险是过拟合与前视偏差。
4. **Look-ahead bias / point-in-time**：using information that was not available at the time; fix = as-of joins on vendor snapshot dates. → 我的 raw → bars → panel 数据面。
5. **Survivorship bias**：only today's surviving stocks in the universe; fix = historical constituents. → A 股 5,500 只全历史宇宙。
6. **Sharpe ratio**：excess return per unit of volatility (annualised). **Deflated Sharpe**：Sharpe adjusted for how many strategies you tried (multiple testing). → 双门之一。
7. **PBO (probability of backtest overfitting)** 与 **purged cross-validation**：CV that removes overlapping samples around the test fold so training doesn't leak into testing. → 双门之一。
8. **Transaction cost / slippage / bps**：commission + spread + market impact; 10 bps = 0.10%. → "excess Sharpe 1.39 net of 10 bps costs"。
9. **Factor / factor risk model**：decompose returns into exposures to common factors (market, size, value, momentum, …) plus idiosyncratic. → 5-factor risk report；2,300 因子目录。
10. **Paper trading**：live loop with real prices but simulated fills. → Alpaca/CCXT 路由、pre-trade risk checks。
11. **Pre-trade risk check**：limits on position size, notional, concentration, leverage before an order goes out. → 我的 paper loop 有；Millennium 的 pod 风险约束是同一思想。
12. **OHLC / VWAP**：open-high-low-close bars; volume-weighted average price. → pc09 Part 2。
13. **As-of query**：the latest value at or before time t. → pc09 Part 1；DuckDB `ASOF JOIN`。
14. **FX conversion / base currency / multi-currency PnL**：convert each position's native-currency value by that day's FX rate; PnL = Δ(price × qty × fx). → pc09 Part 3 / QuantVault OA。
15. **Corporate actions**：splits, dividends, symbol changes that require adjusting price history. → sd01 追问。
16. **Drawdown**：peak-to-trough loss; pods are cut on drawdown limits (folklore says ~5%，不要引用数字). → 说 "tight drawdown limits" 即可。
17. **Settlement / good-funds**：cash and securities actually change hands after a trade (T+1); good-funds = only count money that has settled. → [[S1]] Amex 管线的领域词，可类比后台。
18. **Alpha / signal**：a forecast of relative return; signal evaluation = does it predict out of sample after costs. → 对应 TechPrep "signal evaluation systems"。
