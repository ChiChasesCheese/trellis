---
id: hi-c-lld-rate-limiter-n04-entities
node: lld.problem-breakdowns.rate-limiter.notes
type: qa
step: 4
---
## Q
**限流器 · 实体筛选**｜摘要 · 必会

从需求的名词里，哪些是实体，哪些只是参数或标签？

## A
- **请求：** 在系统之外，我们只拿到 `(clientId, endpoint)` 两个字符串用来查找，没有请求对象的状态和规则，所以是方法参数。
- **客户端：** 客户端本身在系统外，ID 只是"每客户端状态"的键，我们不管理它的生命周期。
- **端点：** 只是用来查配置的标签字符串。
- **限流算法：** 实体。每种算法有专属配置、随算法而变的每键状态、自己的放行规则；不同算法是不同的类。
- **`RateLimiter`：** 实体，协调者：查端点配置、选出算法实例、委托决策。
- **`RateLimitResult`：** 值对象实体：要返回三个值，用结构化类型比散落的基本类型好。很多语言里它不必是类，TypeScript 用类型、Go 用结构体、Python 用 dataclass，关键是类型安全地返回多个值。
- **结果是三个实体：** `RateLimiter`、`Limiter`（接口）、`RateLimitResult`。`RateLimiter` 持有"端点 → `Limiter`"的映射；如何从异构配置造出对应的 `Limiter`，留到类设计。
