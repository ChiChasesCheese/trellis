---
nodes:
- backtest.mechanics.fills
- backtest.mechanics.timing
title: 'Borrowing freqtrade''s Backtest Design: Event-Driven Trade Lists vs Vectorized
  Weights'
url: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/architecture/borrowing-from-freqtrade.md
tags:
- codebase
---

# Borrowing freqtrade's Backtest Design: Event-Driven Trade Lists vs Vectorized Weights

Contrasts two backtest paradigms: freqtrade's event-driven, per-trade simulation, which naturally yields win rate, profit factor, and expectancy because it tracks an explicit trade object, against a vectorized, cross-sectional weights-times-returns-minus-turnover-cost simulation, which is fast and naturally handles many instruments held simultaneously but has no notion of 'one trade' unless one is derived after the fact. Also documents freqtrade's explicit, written-down fill assumptions — orders fill within the candle's high/low range with no slippage, signal exits happen at the next candle's open, stop-losses fill optimistically at the stop price even through a gap — as a model of the assumption-transparency any backtest engine should aim for.

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/quant-stroller/blob/c0cc39c68d33/docs/architecture/borrowing-from-freqtrade.md)

## Archived copy
![[qs-borrowing-freqtrade-backtest-design-clip]]
%% trellis:end %%
