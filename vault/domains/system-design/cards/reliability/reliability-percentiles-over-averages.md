---
id: reliability-percentiles-over-averages
node: reliability.slo
type: qa
---
## Q
Why is p99 latency the SLI to watch instead of the mean — and why does fan-out make tail latency worse than it looks?

## A
Latency is heavily right-skewed: a healthy mean can hide a p99 of seconds, and the slowest requests often belong to your **heaviest users** (biggest carts, most data).

Fan-out amplifies the tail: a page calling 100 backends in parallel is as slow as the slowest one — with p99 = 1s per backend, ~63% of pages (1 − 0.99¹⁰⁰) hit at least one 1-second call. The tail becomes the common case.

## Q zh
为什么 p99 延迟是要看的 SLI 而不是平均值——为什么 fan-out 使尾延迟比看起来更差？

## A zh
延迟严重向右倾斜：健康的平均值可以隐藏秒级 p99，最慢的请求经常属于你**最重用户**（最大购物车、最多数据）。

Fan-out 放大尾：一个调用 100 个后端并行的页面和最慢的一样慢——有 p99 = 1s 每后端，~63% 页面（1 − 0.99¹⁰⁰）击中至少一个 1 秒调用。尾变成常见情况。
