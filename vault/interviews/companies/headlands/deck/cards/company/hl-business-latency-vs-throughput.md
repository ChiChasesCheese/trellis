---
id: hl-business-latency-vs-throughput
node: company.business
type: qa
step: 16
---
## Q
延迟（latency）和吞吐（throughput）分别指什么？为什么二者常此消彼长？

## A
- **延迟**：一件事要多久。
- **吞吐**：单位时间能做多少件。

二者常此消彼长，典型例子是**批量**：把多个请求攒成一批一起处理，能提高吞吐（摊薄每次的固定开销），但每个请求要等批凑齐，延迟变大。

面试里被问网络或存储优化时，这是最安全的框架：先说清目标是延迟还是吞吐，再谈 batching 的取舍。
