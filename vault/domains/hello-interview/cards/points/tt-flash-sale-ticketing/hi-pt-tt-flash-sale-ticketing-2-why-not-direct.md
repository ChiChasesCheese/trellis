---
id: hi-pt-tt-flash-sale-ticketing-2-why-not-direct
node: tt.sd.tt-flash-sale-ticketing.points
type: qa
step: 2
---
## Q
**秒杀抢票 · 为什么不能直接打后端**｜出自：秒杀抢票 › 需求

秒杀抢票为什么不能让 50 万请求/s 直接打到 Redis 或数据库？各自的数字是什么？

## A
**带宽。** 50 万 × 1.5 KB × 8 ≈ 6 Gbps，必须在边缘消化。
**Redis。** 单实例约 5 万次/s，直接打是 10 倍超载。
**数据库单行。** 持锁 2 ms，上限 500/s，失败请求排队耗尽连接池。
**占位量。** 付款转化率 70%，同时占位约 1,000 ÷ 0.7 ≈ 1,429，准入 2,000 略多于所需。
