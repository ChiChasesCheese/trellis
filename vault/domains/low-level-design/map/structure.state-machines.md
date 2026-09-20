%% trellis:begin %%
# 状态机（State Machines）
*API 与程序结构（Program Structure）*

把生命周期（订单、电梯、游戏）建模为显式状态与转移，而不是一锅布尔值。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/low-level-design/map/patterns.state|状态模式（State）]]

**Unlocks:** [[domains/low-level-design/map/problems.machines.elevator|电梯系统（Elevator System）]], [[domains/low-level-design/map/problems.machines.traffic-signal|交通信号灯（Traffic Signal）]], [[domains/low-level-design/map/problems.booking.hotel-booking|酒店预订（Hotel Booking）]], [[domains/low-level-design/map/problems.booking.airline|航班管理（Airline Management）]], [[domains/low-level-design/map/problems.booking.restaurant|餐厅管理（Restaurant Management）]], [[domains/low-level-design/map/problems.marketplaces.online-shopping|在线购物（Amazon）]], [[domains/low-level-design/map/problems.marketplaces.ride-sharing|网约车（Uber）]], [[domains/low-level-design/map/problems.marketplaces.food-delivery|外卖配送（Food Delivery）]], [[domains/low-level-design/map/problems.social.task-management|任务看板（Trello / Jira）]]

## Readings
- [[gpp-state|State (Game Programming Patterns, Bob Nystrom)]]

## Cases
- [[qs-durable-phase-machine-that-decides-nothing|A durable phase machine that decides nothing]] — `quant-stroller`

## Drills
- [[design-airline|Drill：航班管理（Airline Management）]]
- [[design-atm|Drill：ATM 取款机（ATM）]]
- [[design-elevator|Drill：电梯系统（Elevator System）]]
- [[design-food-delivery|Drill：外卖配送（Food Delivery）]]
- [[design-hotel-booking|Drill：酒店预订（Hotel Booking）]]
- [[design-online-shopping|Drill：在线购物（Online Shopping）]]
- [[design-restaurant|Drill：餐厅管理（Restaurant Management）]]
- [[design-ride-sharing|Drill：网约车（Ride Sharing / Uber）]]
- [[design-task-management|Drill：任务看板（Trello / Jira）]]
- [[design-traffic-signal|Drill：交通信号灯（Traffic Signal）]]
- [[design-vending-machine|Drill：自动售货机（Vending Machine）]]

## Cards (5)
1. [[structure-state-enum-vs-boolean-soup]]
2. [[structure-state-transition-table]]
3. [[structure-state-guards-and-illegal-events]]
4. [[structure-state-entry-exit-actions]]
5. [[structure-state-table-vs-state-pattern]]
%% trellis:end %%

## Notes
