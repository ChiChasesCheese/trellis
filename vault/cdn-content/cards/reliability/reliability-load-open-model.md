---
id: reliability-load-open-model
node: reliability.load-testing
type: qa
---
## Q
A closed-loop load test reports stable latency because virtual users wait for each response before sending another request. Why can this hide overload, and what should replace it?

## A
When the service slows, the generator also reduces arrival rate, so offered load collapses exactly when queues should grow. Use an open arrival-rate model for traffic that arrives independently of response time, track dropped iterations, and measure latency from scheduled arrival to completion. Keep a closed model only when it matches real client behavior.

## Q zh
closed-loop load test 显示 latency 稳定，因为 virtual user 会等 response 返回后再发下一个 request。为什么这会隐藏 overload，应该改用什么？

## A zh
service 变慢时，generator 也会降低 arrival rate，因此 offered load 恰好在 queue 应增长时下降。对于独立于 response time 到达的 traffic，应使用 open arrival-rate model，跟踪 dropped iteration，并从 scheduled arrival 到 completion 测量 latency。只有真实 client behavior 确实如此时才保留 closed model。
