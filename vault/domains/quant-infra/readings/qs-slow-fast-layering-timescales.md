---
nodes:
- portfolio.combination
title: 'Slow Sets the Direction, Fast Trades Intraday: Layering Strategies Across
  Timescales'
url: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/deep/slow-fast-layering.md
tags:
- codebase
---

# Slow Sets the Direction, Fast Trades Intraday: Layering Strategies Across Timescales

Distinguishes three genuinely different meanings of 'slow strategy sets direction, fast strategy trades intraday': fast-as-pure-execution (minimizing cost of a decision already made), fast-and-slow-as-fully-independent-alphas with no hierarchy, and fast-constrained-within-a-direction-fence set by the slow layer, where the slow layer gives a direction and a risk budget and the fast layer trades its own intraday signal only inside that budget. Argues, with literature support, that which of the three is correct for a given desk is a matter of capital size, not taste — a fast signal's edge often can't clear round-trip costs for a large book, forcing it down into pure execution, while a small book can let the same signal run as genuine alpha.

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/quant-stroller/blob/c0cc39c68d33/docs/deep/slow-fast-layering.md)

## Archived copy
![[qs-slow-fast-layering-timescales-clip]]
%% trellis:end %%
