---
id: hi-pt-nearby-restaurants-app-10-ranking
node: qb.sd.nearby-restaurants-app.points
type: qa
step: 10
---
## Q
**附近餐厅发现 · 召回与精排**｜追问 · 出自：附近餐厅发现 › 深入 4

附近餐厅首页的排序怎么做？个性化放在哪一层，为什么？

## A
**两阶段。** 先召回（地理加菜系加营业，取前 200 家），再用模型精排（距离、评分、预计送达、转化率、广告）。

**个性化。** 在用户级重排，不进共享缓存，否则缓存键会按用户膨胀，命中率下降。
