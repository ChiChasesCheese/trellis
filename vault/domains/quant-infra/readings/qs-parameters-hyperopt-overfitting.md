---
nodes:
- backtest.overfitting.multiple-testing
- backtest.overfitting.deflated-sharpe
title: Parameters, Hyperparameter Optimization, and the Edge of Overfitting
url: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/deep/parameters-and-hyperopt.md
tags:
- codebase
---

# Parameters, Hyperparameter Optimization, and the Edge of Overfitting

Uses freqtrade's hyperopt, a well-built Bayesian parameter search over trading-rule spaces, as a concrete example of what a good overfitting machine looks like, then explains why searching for the parameter combination that maximizes a backtest metric systematically selects for the combination where luck happened to be largest — the expected maximum Sharpe across N trials rises with N even under pure noise. The discipline that follows is to use one economically-motivated default parameter set rather than sweeping to a peak, and when a sweep is unavoidable, to record the true number of trials searched so a deflated-Sharpe gate can discount the reported result by exactly how hard it was searched for.

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/quant-stroller/blob/c0cc39c68d33/docs/deep/parameters-and-hyperopt.md)

## Archived copy
![[qs-parameters-hyperopt-overfitting-clip]]
%% trellis:end %%
