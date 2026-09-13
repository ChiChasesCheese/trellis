---
id: fnd-capacity-resource-model
node: foundations.capacity
type: qa
---
## Q
How do you turn "we expect 100k QPS" into a defensible server count instead of dividing by a vendor benchmark?

## A
Benchmark the real request mix and measure sustainable QPS **while meeting the latency/error SLO**. Model CPU per request, bytes per request, memory per in-flight request, connection count, cache hit ratio, and downstream quotas; take the minimum capacity across those resources. Then add growth, burst, deployment, and largest-failure-domain headroom and verify with a production-shaped load test.

## Q zh
如何把“预计 100k QPS”变成可辩护的 server count，而不是直接除以 vendor benchmark？

## A zh
用真实 request mix 做 benchmark，并测量在 **满足 latency/error SLO** 时的 sustainable QPS。建模 CPU/request、bytes/request、memory/in-flight request、connection count、cache hit ratio 与 downstream quota；取这些资源中最先达到的 capacity。再加入 growth、burst、deployment 与最大 failure domain 的 headroom，最后用 production-shaped load test 验证。
