%% trellis:begin %%
# 实时持仓与盈亏
*tick-to-trade 系统架构*

由成交回报实时更新持仓、均价、已实现 / 未实现盈亏；为什么持仓要用交易所回报而不是自己的下单记录。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/architecture.order-state|订单状态机与在途订单]]

**Unlocks:** [[domains/hft/map/reliability.monitoring|实时监控与对账]]

## Cards (5)
1. [[hft-architecture-position-pnl-position-from-fills]]
2. [[hft-architecture-position-pnl-why-exchange-fills]]
3. [[hft-architecture-position-pnl-fifo-vs-average-cost]]
4. [[hft-architecture-position-pnl-realized-vs-unrealized]]
5. [[hft-architecture-position-pnl-double-and-bust]]
%% trellis:end %%

## Notes
