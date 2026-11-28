---
id: hi-pt-nearby-restaurants-app-3-precision-boundary
node: qb.sd.nearby-restaurants-app.points
type: qa
step: 3
---
## Q
**附近餐厅发现 · 格子精度与边界**｜必会 · 出自：附近餐厅发现 › 深入 1

附近餐厅的 geohash 网格精度怎么选？用户站在格子边缘时会漏掉什么？

## A
**精度。** 5 位格约 24 km²，市中心每 km² 100 家（假设）则 2,400 家，查 9 格是 21,600 家候选；6 位格约 0.74 km²，3 km 半径面积约 28 km² 要约 38 个格，加边界约 50 个。密度不均，所以用自适应分裂（每叶不超过 100 家）。

**边界。** 近处的店可能在相邻格，必须查周围一圈。
