---
nodes:
- trading.order-lifecycle
- controls.pre-trade
- trading.connectivity
title: 'What an Institutional-Grade Trading Engine Needs: A Requirements Scorecard'
url: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/architecture/live-and-event-driven.md
tags:
- codebase
---

# What an Institutional-Grade Trading Engine Needs: A Requirements Scorecard

A detailed, item-by-item scorecard of what a trading engine needs to be considered correct rather than merely fast: an explicit order state machine with a client-order-id distinct from the venue's id (the join key for reconciliation), idempotent fill processing so a reconnect never double-books a trade, boot-time reconciliation against the venue before the first order of the day, pre-trade risk checks that deny an order before it reaches the venue (fat-finger caps, price collars, kill-switches), and crash-only recovery where startup and disaster-recovery are the same code path. A good checklist of the non-negotiable correctness properties of a live order and risk pipeline, independent of any specific vendor.

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/quant-stroller/blob/c0cc39c68d33/docs/architecture/live-and-event-driven.md)

## Archived copy
![[qs-live-trading-engine-scorecard-clip]]
%% trellis:end %%
