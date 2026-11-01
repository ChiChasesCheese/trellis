---
id: hi-sd-elasticsearch-3-search-geo
node: qb.sd.hotel-booking-system.pre-sd-deep-dives-elasticsearch
type: qa
step: 3
---
## Q
**查询、排序与地理搜索**｜系统设计 · 深入技术

Elasticsearch 的 bool 查询怎么组合文本匹配和范围过滤？排序默认按什么？做 Yelp 或 Uber 这类附近搜索它靠什么？

## A
**查询。** 查询是 JSON，类似 SQL：`bool` 加 `must` 组合 `match`（标题含某词）与 `range`（价格不超过 15）；对 nested 字段要用 `nested` 查询。结果含文档 id、相关度分数和 `_source`。

**排序。** 不指定时按相关度分数 `_score`，默认算法与 TF-IDF 紧密相关；也可按字段、多字段、脚本排序，嵌套字段要用 nested sort。

**地理搜索。** `geo_point` 存经纬度，`geo_shape` 存多边形等区域。`geo_distance` 查半径内的点，可与其他过滤组合，如「2 英里内的意大利餐厅按评分排序」。底层用 BKD 树（k-d 树变体）在二维上快速缩小范围，这比分别给经纬度建 B 树强。
