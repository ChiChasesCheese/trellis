%% trellis:begin %%
# 订单状态机与在途订单
*tick-to-trade 系统架构*

新建、已确认、部分成交、撤单中、已撤、已成交；在途（in-flight）订单与"撤单途中被成交"的竞态。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/hft/map/protocols.ouch|OUCH 下单协议]]

**Unlocks:** [[domains/hft/map/architecture.position-pnl|实时持仓与盈亏]]

## Readings
- [[nasdaq-ouch-5|Nasdaq OUCH 5.0 规范]]

## Drills
- [[architecture-risk-inline-explain|练习：向新同事解释，为什么下单前风控放在热路径里]]

## Cards (5)
1. [[hft-architecture-order-state-states]]
2. [[hft-architecture-order-state-why-state-machine]]
3. [[hft-architecture-order-state-in-flight-risk]]
4. [[hft-architecture-order-state-cancel-race]]
5. [[hft-architecture-order-state-unknown-state]]
%% trellis:end %%

## Notes
