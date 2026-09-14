---
id: fnd-request-trace
node: foundations.request-path
type: qa
---
## Q
A CDN request is slow. Why is "the origin took 80 ms" not an end-to-end diagnosis, and what path should you trace?

## A
Trace the same request through **DNS → connection setup → edge routing → edge cache → shield/regional cache → origin compute → object storage → response transfer**. A fast origin handler can still sit behind slow DNS/TLS, a shield miss, storage I/O, queueing, or a slow response body. Correlate one request ID across hops and assign each segment a latency budget.

## Q zh
一个 CDN 请求很慢。为什么“origin 只用了 80 ms”不算端到端诊断？应该追踪什么路径？

## A zh
沿同一请求追踪 **DNS → connection setup → edge routing → edge cache → shield/regional cache → origin compute → object storage → response transfer**。即使 origin handler 很快，DNS/TLS、shield miss、storage I/O、queueing 或慢速响应体仍可能拖慢请求。用同一个 request ID 串联所有 hop，并给每段分配 latency budget。
