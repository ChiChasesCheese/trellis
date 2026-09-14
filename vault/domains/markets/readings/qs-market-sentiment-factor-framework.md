---
nodes:
- alt-data.positioning
- alt-data.text
title: A Factor Framework for Market Sentiment
url: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/concepts/market-sentiment-factors.md
tags:
- codebase
---

# A Factor Framework for Market Sentiment

A survey of how investor sentiment gets collected (surveys/positioning, options-implied measures, market breadth, fund flows and leverage, and text/NLP), aggregated into composite indices (equal-weighted like CNN Fear & Greed, PCA like Baker-Wurgler, or PLS-optimized like Huang-Jiang-Tu-Zhou), and turned into a tradeable signal. The central lesson is that sentiment's predictive power lives almost entirely in its extremes and in forecasting volatility, not in forecasting the direction of returns in the middle of the range — so the right use is extreme-value mean-reversion or a de-risking overlay, never a smooth bull/bear timing dial, and time-series sentiment bets are exceptionally prone to overfitting given how few independent sentiment cycles exist in history.

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/quant-stroller/blob/c0cc39c68d33/docs/concepts/market-sentiment-factors.md)

## Archived copy
![[qs-market-sentiment-factor-framework-clip]]
%% trellis:end %%
