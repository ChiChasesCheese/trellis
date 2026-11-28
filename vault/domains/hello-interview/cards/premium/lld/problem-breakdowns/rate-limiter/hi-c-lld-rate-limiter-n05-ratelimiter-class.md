---
id: hi-c-lld-rate-limiter-n05-ratelimiter-class
node: lld.problem-breakdowns.rate-limiter.notes
type: qa
step: 5
---
## Q
**限流器 · RateLimiter 的状态与方法**｜摘要 · 必会

`RateLimiter` 该持有什么状态、暴露什么方法？为什么不加 `getConfig`、`updateConfig`？

## A
- **状态两项：** 端点到限流器的映射（常数时间按端点查）；一个默认限流器（所有未配置的端点共享，保证每个请求都受限）。"配置在启动时给出"还要求有办法从配置造限流器，这交给工厂。
- **方法一个：** `allow(clientId, endpoint)`，整个对外 API。构造函数接收配置列表和默认配置。
- **allow 做什么：** 按端点查限流器，查不到用默认，委托给它并把客户端 ID 当键传下去。
- **别加没人要的方法：** 需求没提查询或更新配置时，加 `getConfig`、`updateConfig` 违反 YAGNI（不需要就不做），是常见的"显得全面"的陷阱。
- **构造：** 创建工厂实例，对每个配置取出端点作键、让工厂造限流器、存进映射，最后造默认限流器。全部在启动时完成。
