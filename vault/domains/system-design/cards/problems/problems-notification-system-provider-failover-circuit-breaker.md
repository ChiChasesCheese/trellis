---
id: problems-notification-system-provider-failover-circuit-breaker
node: problems.social.notification-system
type: qa
step: 6
tags: [grown]
---
## Q
A notification system sends push, SMS and email through APNs, Twilio and SendGrid, each with different rate limits and error codes. What is the trade-off between calling each provider's SDK directly from business logic versus building a unified channel-adapter layer, and how does the adapter layer decide to fail over to a backup provider?

## A
Calling provider SDKs directly from business logic gets something working fastest, but each provider's specific error codes (APNs's 410 Unregistered, Twilio's malformed-number errors, SendGrid's bounces) end up scattered across business code with no consistent retry or backoff policy, and adding a new provider means reimplementing that logic again. A unified channel-adapter layer normalizes every provider's errors into a small set of outcomes (permanent_failure, transient_failure, success) behind one interface, and maintains a per-provider rate limiter and circuit breaker; when a provider's circuit breaker trips (its transient-failure rate exceeds a threshold), the adapter automatically routes subsequent sends on that channel to a configured backup provider without business logic being aware a failover happened.

## Q zh
一个通知系统通过 APNs、Twilio、SendGrid 分别发送 push、SMS、email，三者限速规则和错误码都不同。在业务逻辑里直接调用各提供商 SDK，和构建统一的渠道适配层相比，权衡是什么？适配层如何决定故障转移到备用提供商？

## A zh
在业务逻辑里直接调用各提供商 SDK 能最快跑起来，但每个提供商特有的错误码（APNs 的 410 Unregistered、Twilio 的号码格式错误、SendGrid 的退信）会散落在业务代码各处，没有统一的重试/退避策略，新增一个提供商就要重新实现一遍。统一的渠道适配层把每个提供商的错误归一化成少数几种结果（permanent_failure、transient_failure、success），在同一接口背后为每个提供商各自维护限速器和熔断器；当某提供商的熔断器打开（其 transient_failure 比率超过阈值），适配层会自动把该渠道后续的发送路由到配置好的备用提供商，业务逻辑无需感知发生了故障转移。
