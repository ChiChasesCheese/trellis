---
id: traffic-rate-vs-concurrency-limiter
node: traffic.rate-limiting
type: qa
---
## Q
An API gateway runs both a request-rate limiter and a concurrency limiter (Stripe runs both). What does each one cap, and which failure mode does each protect against?

## A
- **Rate limiter** caps **requests per second** per key. Protects against *too many requests*: bursts, runaway retry loops, abusive scripts — volume problems, even when every request is cheap.
- **Concurrency limiter** caps **in-flight requests** (accepted but not yet finished) per key. Protects against *slow or expensive requests*: when the backend degrades and latency rises, a client can stay under its req/s budget while each request holds a worker, connection, and memory for far longer — in-flight count balloons and the resource pool exhausts. Concurrency is a direct proxy for resources held, so this limiter tightens automatically exactly when the system slows down.
- Rule of thumb: rate limiting handles *how often* clients ask; concurrency limiting handles *how long* their requests occupy you. You need the second because the first is blind to latency.

## Q zh
一个 API gateway 同时运行 request-rate limiter 和 concurrency limiter（Stripe 两个都跑）。它们各自限制什么？各自防御哪种故障模式？

## A zh
- **Rate limiter** 限制每个 key 的**每秒请求数**。防御*请求太多*：突发流量、失控的重试循环、滥用脚本 — 数量问题，哪怕每个请求都很便宜。
- **Concurrency limiter** 限制每个 key 的 **in-flight 请求数**（已接受但尚未完成的请求）。防御*慢请求或昂贵请求*：当后端劣化、延迟上升时，客户端可以完全不超 req/s 配额，但每个请求占住 worker、连接和内存的时间大大变长 — in-flight 数膨胀，资源池被耗尽。并发数是所占资源的直接代理，所以这个 limiter 恰好在系统变慢时自动收紧。
- 经验法则：rate limiting 管客户端*问多频繁*；concurrency limiting 管请求*占用你多久*。必须有第二个，因为第一个对延迟是盲的。
