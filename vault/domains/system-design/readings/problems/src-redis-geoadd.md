---
nodes: [problems.geo.proximity]
url: https://redis.io/docs/latest/commands/geoadd/
---
# GEOADD

值得读：Redis 官方命令文档说明了 `GEOADD`/`GEOSEARCH` 的底层实现——把经纬度交织成
52 位整数、存进有序集合（sorted set）、用范围查询模拟半径/矩形搜索，以及它假设地球为
球体（用 Haversine 公式）带来的最坏 0.5% 距离误差。与本题解不同的地方在于：本题解把
这个实现方式作为"geohash 相比 quadtree 更适合高频写入的移动对象（附近好友场景）"这一
结论的具体依据，原文本身只是命令参考，不涉及和其他空间索引结构的取舍讨论。
