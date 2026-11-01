---
id: hi-sd-redis-6-sortedset-geo
node: sd.deep-dives.redis
type: qa
step: 6
---
## Q
**有序集合与地理索引**｜系统设计 · 深入技术

Redis 的有序集合（sorted set）怎样做排行榜或某关键词下的点赞最多的帖子？地理索引的 GEOSEARCH 复杂度为什么是 O(N + log M)？

## A
**要点。** 有序集合按分数维护有序数据，查询是对数时间。例如维护关键词 `tiger` 下点赞最多的帖子：
- `ZADD tiger_posts 500 id1`：设置成员分数，已存在则更新，从而移动排名。
- `ZREMRANGEBYRANK tiger_posts 0 -6`：负索引从最高分数起算，删掉第 0 到倒数第 6 名，只保留前 5 名，定期清理以省空间。

**为什么。** 地理索引（`GEOADD`、`GEOSEARCH`）底层用 geohash（把经纬度编码成一个可排序的值，存在有序集合里）。在有序集合里定位是对数项；geohash 的格子是正方形、与网格对齐，不够精确：第一轮取出格子里的 N 个候选，第二轮再过滤出真正落在半径内的 M 个。

**使用时机。** 排行榜、热门列表、附近的人或点，都先想到这两个结构。
