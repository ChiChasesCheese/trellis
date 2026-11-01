---
id: hi-pt-tt-per-merchant-rate-limit-4-lazy-refill
node: tt.lld.tt-per-merchant-rate-limit.points
type: qa
step: 4
---
## Q
**按商户限流 · 惰性补充令牌**｜出自：按商户限流 › 深入 2

几十万个桶不能各挂一个定时器加令牌。怎么补充？时钟回拨怎么办？用什么时钟？

## A
**做法。** 每次访问补充 `max(0, now − updated) × rate`，上限为突发容量，再把 updated 设为 now。长期不活跃的商户不耗 CPU，只占一个桶内存。
**回拨。** 补充量取 `max(0, ...)`，回拨不产生负数。
**时钟。** 生产用单调时钟（`time.monotonic`），NTP 校时不会打乱令牌；时钟作为构造参数注入，测试用假时钟。
