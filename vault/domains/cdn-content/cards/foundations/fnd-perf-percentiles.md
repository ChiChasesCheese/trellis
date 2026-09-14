---
id: fnd-perf-percentiles
node: foundations.performance
type: qa
---
## Q
An endpoint averages 40 ms but users report frequent 2 s waits. What should replace the average in the investigation?

## A
Inspect the **latency distribution**—at least p50, p95, p99, and p99.9—segmented by hit/miss, region, object size, protocol, and status. A tiny slow population barely moves the mean but dominates user pain, especially when a page fans out to many requests. Pair percentiles with request counts so low-volume slices do not mislead.

## Q zh
一个 endpoint 平均 40 ms，但用户经常遇到 2 秒等待。调查时应该用什么替代 average？

## A zh
查看完整 **latency distribution**——至少 p50、p95、p99、p99.9，并按 hit/miss、region、object size、protocol、status 切分。少量慢请求几乎不影响 mean，却会主导用户痛苦，尤其一个页面 fan out 多个请求时。percentile 必须同时带 request count，避免低流量 slice 误导。
