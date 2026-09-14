---
id: traffic-shedding-response
node: traffic.rate-limiting
type: qa
---
## Q
When a rate limiter rejects a request, what exactly should the response contain — and why does the wrong response amplify load?

## A
- **HTTP 429 Too Many Requests** (or 503 for server-wide shedding) — a distinct code so clients and dashboards can tell throttling from errors.
- **`Retry-After`** header — tells well-behaved clients when to come back, spreading the retry wave.
- **`RateLimit-*` headers** (limit / remaining / reset) — lets clients self-pace before hitting the wall.

Wrong response (generic 500, no Retry-After): clients treat it as transient failure and **retry immediately**, turning shed load into a self-inflicted retry storm.

## Q zh
当速率限制器拒绝请求时，响应确切应该包含什么 — 为什么错误的响应放大负载？

## A zh
- **HTTP 429 Too Many Requests**（或 503 用于服务器范围丢弃）— 一个不同的代码所以客户端和仪表板可以告诉限流来自错误。
- **`Retry-After`** 头 — 告诉行为良好的客户端什么时候回来，传播重试波。
- **`RateLimit-*` 头**（limit / remaining / reset）— 让客户端在打到墙之前自我步调。

错误的响应（通用 500，没有 Retry-After）：客户端将其视为暂时故障并**立即重试**，将丢弃负载变成自我造成的重试风暴。
