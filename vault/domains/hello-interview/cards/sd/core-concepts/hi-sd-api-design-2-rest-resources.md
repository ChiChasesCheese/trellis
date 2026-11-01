---
id: hi-sd-api-design-2-rest-resources
node: sd.core-concepts.api-design
type: qa
step: 2
---
## Q
**REST 的资源建模与参数放哪里**｜系统设计 · 核心概念

REST 接口里资源怎么命名，父子关系用嵌套路径还是查询参数？路径参数、查询参数、请求体各放什么？

## A
**资源建模。** 资源是系统里“存在的东西”（核心实体），不是动作。用复数名词：`/events`、`/events/{id}/tickets`、`POST /events/{id}/bookings`。不要写 `/getUserBookings`、`/processPayment` 这种动作式路径。

**嵌套还是平铺。** 关系必选就用路径（嵌套），如 `/events/{id}/tickets`，不指定是哪场活动就没有意义；过滤条件可选就用查询参数，如 `/tickets?event_id=123&section=VIP`。

**参数放哪。**
- 路径参数：结构性的，决定访问哪个资源
- 查询参数：修饰符，过滤、排序、分页，可选
- 请求体：载荷，创建或更新的核心数据，复杂结构或不适合放进 URL 的内容

例：`POST /events/123/bookings?notify=true`，活动 ID 在路径，是否通知是可选行为放查询参数，票种和数量在请求体。

**易错。** 状态码记常见几个即可：200、201、400、401、404、500，重点是分清 4xx（客户端错）和 5xx（服务端错）。
