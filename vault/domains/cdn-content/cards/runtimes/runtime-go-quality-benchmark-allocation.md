---
id: runtime-go-quality-benchmark-allocation
node: runtimes.go-quality
type: qa
---
## Q
A cache-key function runs on every request. How do you prove an optimization helps rather than merely making code cleverer?

## A
Write a focused benchmark with representative key lengths and header counts, call `b.ReportAllocs()`, and compare stable runs with `benchstat`. Track `ns/op`, `B/op`, and `allocs/op`; isolate setup outside the timed loop. Then profile the end-to-end service, because a microbenchmark win matters only if the function is hot in production. Preserve correctness tests for normalization and collision behavior before optimizing allocations.

## Q zh
cache-key function 在每个请求上执行。如何证明优化真的有效，而不是只让代码更聪明？

## A zh
用有代表性的 key 长度和 header 数写 focused benchmark，调用 `b.ReportAllocs()`，再用 `benchstat` 比较稳定的多次运行。跟踪 `ns/op`、`B/op`、`allocs/op`，把 setup 移出计时循环。随后 profile 端到端服务，因为 microbenchmark 的提升只有在该函数确实是 production hot path 时才有意义。优化 allocation 前，必须保留 normalization 和 collision behavior 的 correctness tests。
