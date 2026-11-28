---
id: hi-c-lld-rate-limiter-n03-final-reqs
node: lld.problem-breakdowns.rate-limiter.notes
type: qa
step: 3
---
## Q
**限流器 · 最终需求与范围外**｜摘要 · 必会

白板上写下哪些需求，哪些被划到范围外？

## A
- **六条需求：**
  1. 配置在启动时一次性提供
  2. 请求是 `(clientId: string, endpoint: string)`
  3. 每个端点配置有：算法名；算法专属参数（令牌桶的 `capacity` 和 `refillRatePerSecond` 等）
  4. 用客户端 ID 对照端点的配置执行限流
  5. 返回结构化结果 `(allowed, remaining, retryAfterMs 或空)`
  6. 端点没有配置时使用默认限制
- **范围外：** 分布式限流（Redis、协调）；动态配置更新；指标和监控；超出基本检查的配置校验。
- **意义：** 明确点名范围外，向面试官表明你想到了它们并选择先不做；其中动态配置、线程安全、内存增长会在扩展里被问回来。
