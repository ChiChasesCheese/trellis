%% trellis:begin %%
# tick-to-trade 系统架构

一套交易系统由哪些组件组成、行情如何在几微秒内变成订单、为什么用单线程事件循环，以及风控、订单状态、回放如何嵌进去。

## Topics
- [[domains/hft/map/architecture.pipeline|交易系统的组件流水线]]
- [[domains/hft/map/architecture.tick-to-trade|tick-to-trade 延迟与预算]]
- [[domains/hft/map/architecture.event-loop|单线程事件循环与忙轮询（busy-spin）]]
- [[domains/hft/map/architecture.hot-cold-path|快路径与慢路径分离]]
- [[domains/hft/map/architecture.threading|线程模型：一核一线程与 SPSC 队列]]
- [[domains/hft/map/architecture.sequencer-journal|定序器、日志与确定性回放]]
- [[domains/hft/map/architecture.pre-trade-risk|内联的下单前风控]]
- [[domains/hft/map/architecture.order-state|订单状态机与在途订单]]
- [[domains/hft/map/architecture.position-pnl|实时持仓与盈亏]]
- [[domains/hft/map/architecture.simulation|回放与交易所模拟器]]
- [[domains/hft/map/architecture.daily-ops|交易系统的一天]]
%% trellis:end %%

## Notes
