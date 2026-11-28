---
id: hi-c-sd-api-design-x02-path-or-query
node: sd.core-concepts.api-design.exam
type: qa
step: 2
---
## Q
**API 设计 · 路径还是查询参数**｜考点 · 必会
设计一个音乐 App 的接口：取某位歌手的所有专辑，可选按发行年份过滤并按热度排序，分页。写出 URL，并说明每个值为什么放那里。

## A
- **URL：** `GET /artists/{artist_id}/albums?year=2020&sort=-popularity&limit=20&cursor=...`
- **`artist_id` 进路径：** 没有它请求不成立，是必需的结构信息。
- **过滤排序分页进查询参数：** `year`、`sort`、`limit`、`cursor` 全是可选修饰，可缺省、可组合。
- **平铺等价写法：** `GET /albums?artist_id=..` 也成立，但它让"artist_id 必填"变成约定而不是 URL 结构；歌手与专辑的父子关系明确，嵌套更清楚。
- **同时说出：** 排序用减号表示降序；其他端点的过滤命名保持一致。
