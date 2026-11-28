---
id: hi-c-sd-postgres-n06-postgis
node: sd.deep-dives.postgres.notes
type: qa
step: 6
---
## Q
**PostgreSQL · 地理查询：PostGIS 与 GiST**｜摘要 · 必会

"查看距我 5 公里内的帖子"在 PostgreSQL 里怎么做？

## A
- **PostGIS 扩展：** 不在内核里，但补上了空间类型和函数；用 `geography` 类型时距离以米为单位。
- **空间索引：** 在位置列上建 GiST 索引（通用索引框架，PostGIS 用包围盒策略），查询 `ST_DWithin(位置, 某点, 5000)` 不必逐行检查。
- **能力：** 点、线、多边形等空间数据；球面距离与平面距离；相交、包含等空间运算；多种坐标系。
- **有多强：** 点和区域的附近查询在中等规模下它完全胜任；位置每秒大量更新时才需要换成 geohash、S2、H3 加内存索引这类专用方案。
- **可组合：** 同一条查询可以同时用全文索引、JSONB 条件和空间条件，得到"旧金山 5 公里内、提到 food、带 restaurant 标签的视频帖"。
- **原则：** 先考虑 PostGIS，再决定是否上专用的地理数据库。
