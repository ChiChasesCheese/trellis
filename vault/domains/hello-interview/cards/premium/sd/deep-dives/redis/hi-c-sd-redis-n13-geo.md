---
id: hi-c-sd-redis-n13-geo
node: sd.deep-dives.redis.notes
type: qa
step: 17
---
## Q
**Redis · 附近搜索：地理空间索引**｜摘要 · 追问

Redis 怎么做"附近的点"？时间复杂度里的 N 和 M 分别是什么？

## A
- **命令：** `GEOADD key 经度 纬度 成员` 加入索引；`GEOSEARCH key FROMLONLAT 经度 纬度 BYRADIUS 半径 单位` 查找。
- **复杂度 O(N + log M)：** 底层用地理哈希（geohash：把经纬度编码成一个可排序的值，存在有序集合里），在有序集合里定位带来对数项。geohash 的格子是对齐网格的方块，不精确：第一遍取出方形格子内的 N 个候选，第二遍再过滤出落在真实半径内的 M 个。
