---
id: hi-c-sd-api-design-n17-versioning
node: sd.core-concepts.api-design.notes
type: qa
step: 17
---
## Q
**API 设计 · 版本策略**｜摘要 · 追问
公开 API 要演进又不能打破旧客户端，URL 版本和请求头版本怎么选？

## A
- **URL 版本：** `/v1/events`、`/v2/events`。显式、一眼可见，路由到不同代码路径也简单；最常用。
- **请求头版本：** `Accept-Version: v2`。URL 更干净、更符合 HTTP 标准，但不直观，在浏览器里也难测试。
- **面试选择：** URL 版本，因为人人理解、解释快。除非被问到请求头版本，否则不展开。
- **留意：** 很多题解甚至不写版本，不是因为不重要（实际生产里重要），而是多数面试官不关心。
