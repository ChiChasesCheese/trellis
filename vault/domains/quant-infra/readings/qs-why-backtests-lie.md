---
nodes:
- data.point-in-time.universe
- features.leakage
- data.quality
title: Why Backtests Lie
url: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/concepts/why-backtests-lie.md
tags:
- codebase
---

# Why Backtests Lie

Walks through four concrete self-deception traps in backtesting: survivorship bias (backtesting on today's index membership silently deletes the losers that mattered), lookahead bias (a signal that quietly uses information not yet available at decision time, caught by re-computing it on truncated data and checking it doesn't change), multiple testing (trying many parameter combinations and reporting only the best one), and corrupted or unadjusted price data (a single bad split-adjustment can manufacture a fake alpha). Each trap is illustrated with a real incident and the automated check built to catch it going forward — a compact, well-chosen orientation to backtest self-deception generally.

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/quant-stroller/blob/c0cc39c68d33/docs/concepts/why-backtests-lie.md)

## Archived copy
![[qs-why-backtests-lie-clip]]
%% trellis:end %%
