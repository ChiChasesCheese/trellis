---
id: hi-c-sd-yelp-n14-location-names
node: sd.problem-breakdowns.yelp.notes
type: qa
step: 14
---
## Q
**Yelp · 深入四：按城市或街区名搜索**｜摘要 · 追问

用户搜"纽约的披萨"或"旧金山 Mission 区"这类地名，系统怎样支持？为什么用半径不行？

## A
- **问题：** 城市、街区不是圆形，形状各异，也不只是邮编、州、城市；固定中心加半径不适用。要用多边形（polygon）表示每个地名所在区域。
- **两个步骤：** (1) 从地名查到多边形；(2) 用多边形过滤范围内的商户。
- **地名到多边形：** 建一张位置表，列有名称（如"San Francisco"）、类型（city、neighborhood）、多边形；数据来自公开数据集（GeoJSON 是常见格式，Geoapify 是一个来源），并对名称列建索引，便于查找。
- **多边形过滤：** Postgres 的 PostGIS 与 Elasticsearch 都支持多边形查询（ES 里给商户文档加 `geo_shape` 字段）。
- **更好：预先计算。** 每次请求都做多边形包含判断不高效。商户创建时就算好它所属的区域，存成一个标识列表（如 `["bay_area","san_francisco","mission_district"]`），在 ES 里对该字段建关键字倒排索引。区域只算一次，之后查询就是一次简单的词项匹配。
