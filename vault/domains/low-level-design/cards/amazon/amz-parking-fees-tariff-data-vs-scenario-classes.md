---
id: amz-parking-fees-tariff-data-vs-scenario-classes
node: amazon.amz-parking-fees
type: qa
step: 5
tags: [grown]
---
## Q
在 Amazon 停车场计费设计里，「车型、时段、周末各有一套逻辑」应该写成一串 if、每个场景一个策略类，还是别的做法？

## A
两种直觉做法都有毛病：一串 if 每加一个场景就要改核心方法；每个场景一个策略类则无法组合，因为一次停留会同时跨过多个场景（夜间加周末）。选择：价目表是数据（`Tariff`），引擎按变价时刻切段，每段单价固定，场景再多也只是改数据或多一个变价时刻。只有出场后的调整（会员折扣、丢票罚款）才用 `Adjustment` 接缝，因为它们有两个真实实现且要按顺序叠加。
