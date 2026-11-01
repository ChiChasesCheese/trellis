---
id: hi-pt-book-seller-platform-3-vendor-isolation
node: qb.sd.book-seller-platform.points
type: qa
step: 3
---
## Q
**图书比价代购平台 · 书商隔离**｜出自：图书比价代购平台 › 深入 1

图书平台里某家书商接口变慢甚至挂掉。平台怎样保证它不拖垮其他书商和整张订单？说出具体机制。

## A
**要点。** 每家书商一个令牌桶限速（token bucket）加独立线程池或信号量（舱壁，bulkhead），慢书商耗尽的只是自己的资源。
**熔断。** 按书商健康度做熔断（circuit breaker），断开期间把它从候选里剔除，整单降级为用剩下的书商比价。
**超时。** 单书商询价超时 1 到 1.5 秒，并行发出。
