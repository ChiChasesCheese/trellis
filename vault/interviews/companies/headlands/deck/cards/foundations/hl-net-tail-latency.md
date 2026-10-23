---
id: hl-net-tail-latency
node: foundations.networking-basics
type: qa
step: 19
---
## Q
为什么交易系统更关心尾延迟？测量尾延迟时要避免什么陷阱？

## A
平均延迟 5 µs、但 1/1000 的请求要 500 µs，这 0.1% 的慢请求往往发生在最关键的时刻（行情剧烈波动时消息最多、处理最慢）。所以用 **p99、p99.9、最大值**衡量。

陷阱是 **coordinated omission**：压测工具在等慢请求时没继续按计划发请求，导致慢请求被低估。
