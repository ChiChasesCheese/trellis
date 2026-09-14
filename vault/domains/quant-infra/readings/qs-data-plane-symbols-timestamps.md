---
nodes:
- data.market-data.time
title: 'The Data Plane: Symbols, Timestamps, and Two Backtest Worlds'
url: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/architecture/data-flow.md
tags:
- codebase
---

# The Data Plane: Symbols, Timestamps, and Two Backtest Worlds

Explains the universal-identifier pattern of tagging every instrument with a market-prefixed symbol so each layer of a system can dispatch on that one prefix, and works through a genuinely tricky correctness detail: storing daily bars at a UTC-midnight timestamp is a storage convention, not the real close time, so a naive same-day join across two markets in different timezones can accidentally let one market's signal see information from later in the trading day than it should. A useful worked example of how timezone and session-calendar handling can silently introduce lookahead bias across markets that trade on different clocks.

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/quant-stroller/blob/c0cc39c68d33/docs/architecture/data-flow.md)

## Archived copy
![[qs-data-plane-symbols-timestamps-clip]]
%% trellis:end %%
