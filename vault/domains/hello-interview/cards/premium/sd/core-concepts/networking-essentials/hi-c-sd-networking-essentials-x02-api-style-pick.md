---
id: hi-c-sd-networking-essentials-x02-api-style-pick
node: sd.core-concepts.networking-essentials.exam
type: qa
step: 2
---
## Q
**网络基础 · API 风格怎么选**｜考点 · 必会

三个场景：(1) 对外公开的开放平台；(2) 内部微服务之间高吞吐调用；(3) 移动端首页需要聚合很多资源且需求不断变化。各用什么？

## A
- **(1) REST：** 对外客户端不受你控制，JSON over HTTP 工具链成熟，易调试，gRPC 的二进制协议对它们不友好。
- **(2) gRPC：** 强类型、二进制、HTTP/2，内部服务延迟主要在网络时收益大；对外仍用 REST，内外分开使用是常见做法。
- **(3) GraphQL：** 前端迭代快，一个查询取回所需字段，避免欠取和过取。但它给后端带来执行复杂度。
- **面试默认：** REST。只有题目强调灵活性或需求不确定时提 GraphQL，不要在其他瓶颈未处理前过度优化 RPC 协议。
