---
id: hi-pt-parking-lot-system-1-strategies
node: qb.lld.parking-lot-system.points
type: qa
step: 1
---
## Q
**停车场管理系统 · 两个变化点做成策略**｜出自：停车场管理系统 › 核心实体与接口

停车场设计里变化最频繁的是什么？各用什么模式隔离？核心类怎么分工？

## A
**要点。** 车位分配策略和计费规则会变，做成两个可替换策略：`SpotAllocator`（`allocate`/`release`，实现 `NearestFirstAllocator`）和 `FeePolicy`（`fee(entered, exited)`，实现 `TieredFee`）。
**类。** `Spot`、`Ticket`（票号、车牌、车位、入场时间）、`ParkingLot` 门面（`enter`、`exit`）。
**好处。** 加计费规则或电动车位只增代码，不改流程。
