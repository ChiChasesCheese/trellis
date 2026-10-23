%% trellis:begin %%
# 交易系统的组件流水线
*tick-to-trade 系统架构*

feed handler → 订单簿 → 策略 → 风控 → 下单网关（order gateway），以及旁路的 OMS、持仓、日志、监控。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/protocols.feed-handler|feed handler 的职责]]

**Unlocks:** [[domains/hft/map/architecture.tick-to-trade|tick-to-trade 延迟与预算]], [[domains/hft/map/architecture.event-loop|单线程事件循环与忙轮询（busy-spin）]], [[domains/hft/map/architecture.pre-trade-risk|内联的下单前风控]], [[domains/hft/map/fpga.trading-uses|FPGA 在交易系统中的用法]]

## Readings
- [[wiki-algorithmic-trading|算法交易（algorithmic trading）]]

## Cards (5)
1. [[hft-architecture-pipeline-components]]
2. [[hft-architecture-pipeline-side-components]]
3. [[hft-architecture-pipeline-budget-example]]
4. [[hft-architecture-pipeline-run-to-completion-vs-pipeline]]
5. [[hft-architecture-pipeline-slow-stage-blocks]]
%% trellis:end %%

## Notes
