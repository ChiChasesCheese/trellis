---
nodes:
- portfolio.sizing
- execution.impact
title: 'From Signal to Trade: Kelly Sizing, Risk Parity, and Cost-Aware Execution'
url: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/architecture/citadel-research-and-sizing.md
tags:
- codebase
---

# From Signal to Trade: Kelly Sizing, Risk Parity, and Cost-Aware Execution

Lays out the chain from a validated signal to an executable, appropriately-sized trade: the Grinold-Kahn fundamental law (information ratio roughly equals skill times root breadth) as the master equation for why many independent small edges beat one big one; the Kelly criterion for growth-optimal position sizing and why practitioners run a fraction of full Kelly; hierarchical risk parity for building a diversified portfolio without inverting a poorly-conditioned covariance matrix; and the Almgren-Chriss and Gârleanu-Pedersen frameworks for trading a target position into an actual book at minimum cost given how fast the signal itself decays. A concise map connecting 'the edge is real' to 'here is how much of it to trade, and how.'

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/quant-stroller/blob/c0cc39c68d33/docs/architecture/citadel-research-and-sizing.md)

## Archived copy
![[qs-citadel-research-sizing-chain-clip]]
%% trellis:end %%
