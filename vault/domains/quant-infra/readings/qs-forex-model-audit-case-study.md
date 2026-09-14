---
nodes:
- data.quality
- backtest.overfitting.multiple-testing
title: 'Case Study: Auditing an FX Deep-Learning Model''s Synthetic-Pair Mirage'
url: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/deep/forex-model-audit.md
tags:
- codebase
---

# Case Study: Auditing an FX Deep-Learning Model's Synthetic-Pair Mirage

A forensic audit of an external FX deep-learning model that self-reported an implausible Sharpe of 2.7 and near-record cumulative returns, run through an honesty pipeline without retraining it. The diagnosis: nearly all the apparent edge lived in synthetic currency pairs that are computed, not traded, whose fabricated price bounces come from stale two-leg quoting; splitting tradable from untradeable instruments collapsed the hit rate to a coin flip. A genuinely useful confident-subset signal survived on two real pairs but reduced to roughly two independent bets across two years of data — real but far too thin to deploy. A reusable checklist for auditing any 'too good' backtest closes the piece.

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/quant-stroller/blob/c0cc39c68d33/docs/deep/forex-model-audit.md)

## Archived copy
![[qs-forex-model-audit-case-study-clip]]
%% trellis:end %%
