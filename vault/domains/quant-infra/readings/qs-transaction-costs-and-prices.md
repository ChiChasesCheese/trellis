---
nodes:
- backtest.mechanics.costs
- execution.impact
- execution.spread
title: The Truth About Trading Costs and Prices
url: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/deep/costs-and-prices.md
tags:
- codebase
---

# The Truth About Trading Costs and Prices

Covers transaction costs from first principles: why OHLCV holds more information than the close alone (an overnight-vs-intraday return split, with a documented overnight-return premium); the bid-ask spread as the first cost and the Corwin-Schultz high-low estimator for it when tick data isn't available, including a worked example of why that estimator badly overstates spreads for liquid large caps; the square-root market-impact law as the second cost; and why total cost scales with turnover, which is why short-horizon signals are especially vulnerable to being gross-positive and net-negative. Ends with a signal that looked like the strongest in a whole research program until realistic costs were applied.

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/quant-stroller/blob/c0cc39c68d33/docs/deep/costs-and-prices.md)

## Archived copy
![[qs-transaction-costs-and-prices-clip]]
%% trellis:end %%
