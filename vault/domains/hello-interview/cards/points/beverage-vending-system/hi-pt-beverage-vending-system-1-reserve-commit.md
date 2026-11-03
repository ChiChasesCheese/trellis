---
id: hi-pt-beverage-vending-system-1-reserve-commit
node: qb.lld.beverage-vending-system.points
type: qa
step: 2
---
## Q
**多地点饮品自助售卖系统 · 库存预留与提交分离**｜必会 · 出自：多地点饮品自助售卖系统 › 深入 1

多地点饮品售卖系统里，两个订单同时读到「还剩一杯的原料」，先查后扣会超卖。库存怎么设计才能不超卖，制作失败时怎么办？

## A
**要点。** `Inventory` 维护实际量和已预留量，可用量 = 实际量 − 已预留量；`reserve` 在锁内整体检查并占用（全有或全无）。
**提交。** 制作成功 `commit`（预留转真实消耗）；失败 `release`（只归还预留）。
**为什么。** 把「承诺」和「消耗」分开，制作期间别的订单看到的可用量已扣掉，故障恢复简单。
