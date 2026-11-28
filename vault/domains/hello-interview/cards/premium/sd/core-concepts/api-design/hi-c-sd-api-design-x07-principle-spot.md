---
id: hi-c-sd-api-design-x07-principle-spot
node: sd.core-concepts.api-design.exam
type: qa
step: 7
---
## Q
**API 设计 · 找出违反的原则**｜考点 · 必会
评审一个接口：①`GET /orders` 返回全部订单；②`GET /orders/9/cancel` 会取消订单；③错误统一返回 200，体里 `{"success":false}`；④登录态存在服务器内存里。分别违反哪条原则，后果是什么？

## A
- **① 违反"可增长集合要分页"：** 小数据时没问题，订单上到几百万行会拖垮数据库和网络；需要分页和页大小上限。
- **② 违反最小惊讶（GET 不能改数据）：** 浏览器预取、爬虫、缓存都可能无意触发取消，而且 GET 本应可重复安全执行。改用 `POST /orders/9/cancellation` 或 `DELETE`。
- **③ 违反最小惊讶和可操作错误：** 监控、重试、缓存看状态码；全是 200，故障看不见。应使用 4xx/5xx 加错误码。
- **④ 违反无状态：** 请求必须落到有会话的那台机器，扩容和故障转移变难。可用 JWT 或集中式会话存储。
