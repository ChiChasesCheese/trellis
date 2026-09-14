---
nodes:
- controls.limits
- trading.accounting
title: freqtrade's Full Architecture, Subsystem by Subsystem
url: https://github.com/quant-stroller/blob/c0cc39c68d33/docs/architecture/freqtrade-full-comparison.md
tags:
- codebase
---

# freqtrade's Full Architecture, Subsystem by Subsystem

A subsystem-by-subsystem tour of what a mature single-asset live trading bot needs beyond the backtest engine itself: a protections state machine that locks trading after triggering conditions (stop-loss guard, max-drawdown, cooldown-after-exit) rather than only checking pre-trade; a wallets/persistence layer that tracks available capital and survives a restart without re-submitting orders; and a remote-control layer for an unattended bot. Useful as a checklist of what production-grade live infrastructure is generally expected to include — order-state tracking, capital bookkeeping, and post-trigger lockouts — independent of which specific bot framework is being read about.

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/quant-stroller/blob/c0cc39c68d33/docs/architecture/freqtrade-full-comparison.md)

## Archived copy
![[qs-freqtrade-full-architecture-tour-clip]]
%% trellis:end %%
