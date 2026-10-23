%% trellis:begin %%
# tick-to-trade 延迟与预算
*tick-to-trade 系统架构*

从行情包到达网卡到订单包离开网卡的时间（wire-to-wire），各环节的典型预算，以及软件 / FPGA 系统的量级。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/architecture.pipeline|交易系统的组件流水线]], [[domains/hft/map/overview.why-speed|为什么速度决定盈亏]]

**Unlocks:** [[domains/hft/map/measurement.budget-method|延迟预算与排查方法]]

## Cards (5)
1. [[hft-architecture-tick-to-trade-definition-wire-to-wire]]
2. [[hft-architecture-tick-to-trade-software-vs-fpga-magnitude]]
3. [[hft-architecture-tick-to-trade-colocation-and-distance]]
4. [[hft-architecture-tick-to-trade-budget-tail-not-average]]
5. [[hft-architecture-tick-to-trade-relative-speed]]
%% trellis:end %%

## Notes
