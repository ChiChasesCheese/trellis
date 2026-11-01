---
id: hi-pt-rate-limiter-system-8-algo-choice
node: qb.lld.rate-limiter-system.points
type: qa
step: 8
---
## Q
**限流器（单机类设计） · 算法怎么选**｜出自：限流器（单机类设计） › 深入 3

面试里被问「选哪种限流算法」，依据是什么？

## A
**依据。** 要「严格每 T 秒不超过 N」选滑动窗口日志；要「平均速率受限但允许一定突发」选令牌桶。
**打法。** 面试里先实现一种，说出其他几种的差别，再按要求补一个。
