---
nodes:
- backtest.overfitting.multiple-testing
- backtest.overfitting.deflated-sharpe
- backtest.overfitting.pbo
title: 'Why ''It Worked on the Test Set'' Isn''t Enough: Multiple Testing and Backtest
  Overfitting'
url: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/concepts/multiple-testing.md
tags:
- codebase
---

# Why 'It Worked on the Test Set' Isn't Enough: Multiple Testing and Backtest Overfitting

The foundational argument for why a single backtest Sharpe ratio is uninterpretable without knowing how many strategies were tried: under pure noise, the expected maximum Sharpe across N trials rises with N, so an out-of-sample test that gets looked at and re-queried repeatedly becomes a second training set (the reusable-holdout problem). It walks through Deflated Sharpe, Harvey-Liu Bonferroni haircuts, combinatorial purged cross-validation, and the probability of backtest overfitting as the standard toolkit for correcting this, and makes the case, with citations to the founding papers, that a high rejection rate in a research pipeline is a sign of a working filter, not a failure.

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/quant-stroller/blob/c0cc39c68d33/docs/concepts/multiple-testing.md)

## Archived copy
![[qs-multiple-testing-backtest-overfitting-clip]]
%% trellis:end %%
