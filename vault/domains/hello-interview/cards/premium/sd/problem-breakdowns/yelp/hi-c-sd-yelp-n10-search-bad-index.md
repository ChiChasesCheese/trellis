---
id: hi-c-sd-yelp-n10-search-bad-index
node: sd.problem-breakdowns.yelp.notes
type: qa
step: 10
---
## Q
**Yelp · 深入三：为什么普通 B 树索引搜不动位置**｜摘要 · 必会

按经纬度矩形加名称查商户，为什么直接查很慢，在经纬度上建 B 树索引为什么也不够？

## A
- **直接查：** `latitude > a AND latitude < b AND longitude > c AND longitude < d AND name LIKE '%coffee%'` 要全表扫描逐行检查；对名称的通配符 `LIKE` 也无法用普通索引。
- **B 树索引的局限：** 在 (latitude, longitude) 上建复合索引，理想中能加速矩形查询，其实效果有限：
  - 范围查询：B 树擅长一维范围，对两个维度同时的范围就吃力；
  - 缺乏空间感知：B 树把经度和纬度当两个独立的值，不理解二维邻近关系。
- **出路：** 需要为空间数据设计的索引结构，如 R 树、四叉树（quadtree）或基于 geohash 的索引。
- **三类过滤要三种索引：** 位置用地理索引；名称用全文索引（倒排索引）；类别用普通 B 树。
