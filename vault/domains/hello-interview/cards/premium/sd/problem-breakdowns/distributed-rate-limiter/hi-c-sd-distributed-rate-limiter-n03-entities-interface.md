---
id: hi-c-sd-distributed-rate-limiter-n03-entities-interface
node: sd.problem-breakdowns.distributed-rate-limiter.notes
type: qa
step: 3
---
## Q
**分布式限流器 · 实体与接口**｜摘要 · 必会

限流器有哪些核心实体？对外的接口只有一个，参数和返回值为什么这样设计？

## A
- **规则（Rules）：** 限流策略，包含时间窗口内的次数、适用哪类客户端、覆盖哪些端点。例如"登录用户每小时 1000 次"、"搜索接口每个 IP 每分钟 10 次"。
- **客户端（Clients）：** 被限流的对象，可以是用户 ID、IP、API key 或它们的组合，每个客户端都有对应当前用量的状态。
- **请求（Requests）：** 带着客户端身份、访问的端点、时间戳的 API 请求，决定适用哪些规则、怎样记账。
- **协作：** 请求到达 → 识别客户端 → 找到适用规则 → 检查当前用量 → 允许或拒绝。
- **接口：** 限流器是别的服务来调用的基础设施，只需要一个方法：
  `isRequestAllowed(clientId, ruleId) → { passes, remaining, resetTime }`
  - 输入是客户端标识和规则标识；
  - 返回是否放行，以及用于 `X-RateLimit-Remaining`、`X-RateLimit-Reset` 响应头的信息。
- **口述侧重：** 这题常见的走法是简单带过实体和接口，把时间花在算法和扩容上；不同面试官的侧重差异很大（有的要代码，有的要架构），开场可以问清。
