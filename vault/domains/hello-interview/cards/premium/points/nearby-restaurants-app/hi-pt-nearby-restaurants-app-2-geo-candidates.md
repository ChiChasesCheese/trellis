---
id: hi-pt-nearby-restaurants-app-2-geo-candidates
node: qb.sd.nearby-restaurants-app.points
type: qa
step: 2
---
## Q
**附近餐厅发现 · 地理候选与精确过滤**｜必会 · 出自：附近餐厅发现 › 深入 1

按位置和半径搜附近餐厅，geohash 网格怎么用？为什么查询结果还要再过滤一次？

## A
**做法。** 把圆形半径转换成覆盖它的格子，格子里的点是超集（候选），再用球面距离（haversine）精确过滤，因为边界格子里有圈外的点。

**实现选择。** 100 万个点，搜索引擎的地理字段能同时解决半径、菜系、关键词和打分，不用自己拼。
