---
nodes:
- regimes.volatility
- volatility.vrp
title: Macro Regime and Position Sizing
url: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/concepts/macro-regime-and-sizing.md
tags:
- codebase
---

# Macro Regime and Position Sizing

Reports a cross-market empirical finding: a macro risk-off state (built from the yield curve, VIX, and credit spreads) reliably predicts higher forward volatility in equities, EM stocks, and FX, but does not reliably predict the direction of forward returns — in fact stocks and FX often bounce after risk-off readings. The conclusion is a sizing rule, not a timing rule: use macro state to scale position size down ahead of volatility spikes (forward-looking vol targeting), never as a binary sell-the-market signal, since that misfires badly in V-shaped selloffs like COVID. A variance-risk-premium overlay is separately noted as one of the few de-risking signals that actually held up.

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/quant-stroller/blob/c0cc39c68d33/docs/concepts/macro-regime-and-sizing.md)

## Archived copy
![[qs-macro-regime-sizing-clip]]
%% trellis:end %%
