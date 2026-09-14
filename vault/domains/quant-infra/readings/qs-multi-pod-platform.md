---
nodes:
- portfolio.pod-allocation
title: 'Multi-pod platform: risk and capital across autonomous teams'
url: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/concepts/citadel-multi-pod-platform.md
tags:
- codebase
---

# Multi-pod platform: risk and capital across autonomous teams

A walk through the multi-manager shape — many autonomous alpha pods sitting under a two-tier risk system, with a per-pod drawdown stop-out beneath a firm-level gross cap. Read it for the allocation loop rather than the org chart: capital moves toward pods by Sharpe, damped by a correlation penalty that down-weights a pod duplicating exposure the book already carries. The part worth arguing with is the failure mode it names — pod correlations that look comfortably low in calm markets converge on one exactly when the gross cap matters, so the diversification the allocator priced in is gone at the moment it is needed.

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/quant-stroller/blob/c0cc39c68d33/docs/concepts/citadel-multi-pod-platform.md)

## Archived copy
![[qs-multi-pod-platform-clip]]
%% trellis:end %%
