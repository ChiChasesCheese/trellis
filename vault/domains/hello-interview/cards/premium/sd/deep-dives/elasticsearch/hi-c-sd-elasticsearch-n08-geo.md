---
id: hi-c-sd-elasticsearch-n08-geo
node: sd.deep-dives.elasticsearch.notes
type: qa
step: 8
---
## Q
**Elasticsearch · 地理空间搜索**｜摘要 · 必会

Elasticsearch 的两种地理类型是什么？怎么查附近？底层靠什么变快？

## A
- **`geo_point`：** 一个经纬度点，适合餐厅位置、签到、送货地址。
- **`geo_shape`：** 任意几何形状（多边形、线、圆、边界框），适合配送区、城市边界、服务覆盖范围。
- **用法：** 映射里声明字段类型；加文档时带上坐标；`geo_distance` 查询在某点指定距离内（如 5 km）的文档；可以放进 `bool` 与其他过滤、排序组合（例如两英里内按评分排序的意大利餐厅）。
- **底层：** 底层是 BKD 树（针对块存储优化的 k-d 树变体）。`geo_point` 用 BKD 树索引坐标，能在二维上直接缩小搜索范围，不像分别对纬度和经度建 B 树那样受限。对 Yelp、Uber 这类位置服务，这是它相对关系库的优势。
