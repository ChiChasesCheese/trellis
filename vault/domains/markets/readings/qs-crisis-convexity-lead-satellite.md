---
nodes:
- regimes.volatility
- momentum.trend
title: 'Crisis Convexity vs Short Premium: Who Leads, Who Rides Along'
url: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/concepts/crisis-convexity-vs-short-premium.md
tags:
- codebase
---

# Crisis Convexity vs Short Premium: Who Leads, Who Rides Along

Argues that correlation between strategies is regime-dependent, not a fixed number: strategies that sell insurance (carry, credit, short volatility) look attractively uncorrelated in calm markets, but their hidden short-volatility exposure converges to correlation 1 exactly when a crisis hits, while trend-following and some value trades pay off convexly in the same crisis because their payoff is structurally long optionality. The piece turns this into an allocation rule — put crisis-convex, positively-skewed strategies in the core position and treat short-premium strategies as tightly-capped satellites — and warns that a low correlation measured in a quiet sample is not evidence it will hold up in a crisis.

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/quant-stroller/blob/c0cc39c68d33/docs/concepts/crisis-convexity-vs-short-premium.md)

## Archived copy
![[qs-crisis-convexity-lead-satellite-clip]]
%% trellis:end %%
