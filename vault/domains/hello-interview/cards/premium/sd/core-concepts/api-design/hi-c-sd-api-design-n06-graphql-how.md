---
id: hi-c-sd-api-design-n06-graphql-how
node: sd.core-concepts.api-design.notes
type: qa
step: 6
---
## Q
**API 设计 · GraphQL · 为何出现、怎么用**｜摘要 · 必会
GraphQL 解决了 REST 的什么痛点？它的请求长什么样，面试里什么时候该提？

## A
- **痛点：** 移动端和网页端需要的数据不同。REST 只有两条路：为每种用途开新接口（接口越开越多、改动要等后端发版），或让接口返回所有人可能需要的全部字段（手机下载一堆用不上的数据，即 over-fetching）。
- **做法：** 只有一个入口，客户端发送一段查询，声明要的字段和关联，如 `event(id) { name date venue { name } tickets { price } }`，服务器按这个形状返回，一次请求取完关联数据（解决 under-fetching，不用来回多次请求）。
- **适合：** 客户端多样、前端要快速迭代而不想等后端改接口。
- **代价：** 要实现查询解析、模式校验，缓存也比"一个 URL 一个缓存项"复杂。
- **面试策略：** 看到明确的多取/少取问题时才提，不作为默认；先用简单工具解决核心架构问题。
