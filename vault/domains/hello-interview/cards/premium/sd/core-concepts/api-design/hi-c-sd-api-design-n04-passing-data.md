---
id: hi-c-sd-api-design-n04-passing-data
node: sd.core-concepts.api-design.notes
type: qa
step: 4
---
## Q
**API 设计 · REST · 参数放哪里**｜摘要 · 必会
请求里的数据该放进路径、查询参数还是请求体？一个预订请求怎么分配？

## A
- **路径参数（结构）：** 标识"是哪一个资源"，缺了请求无意义，如 `/events/123`。
- **查询参数（修饰）：** 过滤、排序、分页，可选、可叠加，如 `/events?city=NYC&limit=20`；第一个参数用 `?` 开头，后面的用 `&` 连接。
- **请求体（载荷）：** 要创建或更新的实际数据；结构复杂、体积大、或不宜出现在 URL 里（URL 会进日志和浏览器历史）的内容放这里。
- **例子：** `POST /events/123/bookings?notify=true` 加 JSON 体（票种、数量、支付方式）。活动编号必需，所以进路径；是否通知是可选行为，所以进查询参数；订单明细是核心数据，所以进请求体。
