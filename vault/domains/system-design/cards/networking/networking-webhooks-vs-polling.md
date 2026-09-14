---
id: networking-webhooks-vs-polling
node: networking.api-styles
type: qa
---
## Q
Exposing events to third-party integrators: webhooks vs letting them poll. What must a webhook provider build that polling gives for free?

## A
Delivery machinery, because consumer endpoints are down or slow constantly:

- **Retries with backoff + dead-letter handling** — and since retries reorder and duplicate, consumers need event ids and idempotent handlers.
- **Authentication of pushes**: HMAC-signed payloads so receivers can verify origin.
- **A replay/list API anyway** — consumers must recover after missing deliveries.

Polling is simpler and consumer-paced, but latency = poll interval and most polls return nothing. Robust pattern: webhook as a "something changed" ping; consumer fetches truth via the API.

## Q zh
向第三方集成商公开事件：webhook vs 让他们轮询。webhook 提供商必须构建什么轮询免费给的？

## A zh
交付机制，因为消费者端点是宕机或缓慢的不断：

- **带退避的重试 + 死信处理** — 并且因为重试重新排序并重复，消费者需要事件 ID 和幂等处理程序。
- **推送的身份验证**：HMAC 签名的有效载荷所以接收者可以验证源。
- **无论如何重放/列表 API** — 消费者必须在缺少交付后恢复。

轮询更简单且消费者步调，但延迟 = 轮询间隔且大多数轮询返回无。强大的模式：webhook 作为"某事改变"ping；消费者通过 API 获取真实。
