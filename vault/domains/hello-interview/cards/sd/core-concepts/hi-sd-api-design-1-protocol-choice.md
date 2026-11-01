---
id: hi-sd-api-design-1-protocol-choice
node: qb.sd.book-seller-platform.pre-sd-core-concepts-api-design
type: qa
step: 1
---
## Q
**面试里怎么选 API 协议**｜系统设计 · 核心概念

系统设计面试的 API 环节，REST、GraphQL、RPC 怎么选？面试官的哪些提示该让你换协议？这一环节该花多少时间？

## A
**要点。** 默认 REST：基于 HTTP 方法和 URL 操作资源，天然对应数据库的增删改查，工具成熟，约九成场景适用，拿不准就说“用 REST”然后继续。

**换协议的信号。**
- 面试官提到“灵活取数”“避免 over-fetching / under-fetching”（取多了或取少了），想到 GraphQL
- 提到微服务、内部接口、高性能、多语言，想到 RPC（如 gRPC）
- 通知、聊天、实时推送，这不是传统 API，是持久连接，用 WebSocket 或 SSE

**数字。** 面试官多半不在意 API 是否完美，只想看到你能设计出合理的接口，然后去做更难的部分。API 环节别超过约 5 分钟，候选人更常见的错误是在这里花太久。

**取舍。** 面向外部客户端的接口用 REST，内部服务间通信可以说一句“走 RPC”，通常不展开内部接口。
