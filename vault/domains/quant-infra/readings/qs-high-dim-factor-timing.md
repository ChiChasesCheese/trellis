---
nodes:
- portfolio.risk-models.covariance
- portfolio.combination
title: 'High-Dimensional Factor Timing: Shrinkage Discipline and the Dimension × Sample-Length
  Law'
url: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/deep/high-dim-factor-timing.md
tags:
- codebase
---

# High-Dimensional Factor Timing: Shrinkage Discipline and the Dimension × Sample-Length Law

Replicates and extends a 2025 academic result that factor timing, dynamically overweighting factors expected to do well, works only under two joint conditions: enough factors to time (dimension) and enough history to identify the timing weights without overfitting (sample length). A three-layer shrinkage scheme, toward a scaled identity, toward the static portfolio, and a gross-exposure rescale, is what keeps naive timing from collapsing in high dimensions, and a controlled dimension-ladder experiment shows the timing premium can flip from strongly positive to strongly negative when the same dimension increase happens on a short sample — a caution against timing new markets before they have 15-20 years of history.

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/quant-stroller/blob/c0cc39c68d33/docs/deep/high-dim-factor-timing.md)

## Archived copy
![[qs-high-dim-factor-timing-clip]]
%% trellis:end %%
