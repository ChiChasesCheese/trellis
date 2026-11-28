---
id: hi-c-sd-proximity-search-n11-geohash-prefix
node: sd.deep-dives.proximity-search.notes
type: qa
step: 11
---
## Q
**邻近搜索 · 前缀相同为什么靠近，以及 Redis 里的用法**｜摘要 · 必会

为什么 geohash 能用任何有序索引做邻近查询？Redis 的 geo 命令是怎么做的？

## A
- **前缀即邻近：** 两个点共享前缀，说明它们在前缀覆盖的每一层都落在同一个格子里；每多共享一个字符，共享的格子就更小。共享 5 个字符，在同一个约 5 公里的方块里；共享 6 个，缩到约 1 公里。
- **可预测的局部性：** 因此在任何数据库的任何有序索引上都能做邻近查询：`WHERE geohash LIKE 'dr5ru%'` 就是普通 B 树的前缀扫描。
- **Redis：** `GEOADD` 把经纬度交错成一个 52 位的 geohash 整数，作为分数存进有序集合；附近查询变成对分数的 `ZRANGEBYSCORE` 范围扫描，原理就是前缀扫描换了写法。
- **注意方向：** 前缀相同通常意味着靠近，但前缀不同不一定远，见下一张。
