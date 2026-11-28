---
id: hi-c-sd-api-design-n14-graphql-schema
node: sd.core-concepts.api-design.notes
type: qa
step: 14
---
## Q
**API 设计 · GraphQL · 模式与 N+1**｜摘要 · 追问
选了 GraphQL，设计工作变成什么？它最大的坑 N+1 是什么，怎么处理？字段级授权又是什么？

## A
- **设计对象换成模式（schema）：** 定义类型和类型之间的关系（Event 有一个 Venue、一组 Ticket），再用 `Query` 声明入口，如 `event(id)`、`events(limit, after)`。客户端沿关系一次遍历。
- **N+1 问题：** 查 100 个活动及其场馆，朴素的解析器（resolver）先 1 次查活动，再为每个活动单独查一次场馆，共 101 次数据库查询，而理想是 2 次。
- **解法：** 批处理（DataLoader 一类）把同一轮里的多个同类查找合并成一次 `WHERE id IN (...)`；代价是多了一层要维护的机制，REST 没有这个问题。
- **授权在字段级：** REST 保护的是整个端点，GraphQL 可以让同一用户看得到活动名称却看不到场馆数据，在 resolver 里按字段判断。
