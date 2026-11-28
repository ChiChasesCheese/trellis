---
id: hi-c-sd-proximity-search-x06-redis-or-postgis
node: sd.deep-dives.proximity-search.exam
type: qa
step: 8
---
## Q
**邻近搜索 · 司机用 Redis 还是 PostGIS**｜考点 · 追问

一个叫车服务 100 万个在线司机，每 4 秒上报一次位置。存在 Redis geo 里还是 PostGIS 里？配送区域判断呢？

## A
- **写入量：** 100 万 / 4 秒 = 每秒 25 万次更新。
- **司机位置用 Redis geo：** 每次更新是有序集合里的一次写入，内存里完成，轻松承受；加过期时间（TTL）清理离线司机。
- **PostGIS 放不下这个写入：** 每次更新要改 R 树，且每次更新产生新的行版本和 WAL 写入，25 万 QPS 对单节点太重。
- **配送区域判断用 PostGIS：** 多边形包含要用 R 树和精确几何运算，变化少、查询多，是它擅长的。
- **组合：** 位置放 Redis，区域规则放 PostGIS，两者各取所长。
