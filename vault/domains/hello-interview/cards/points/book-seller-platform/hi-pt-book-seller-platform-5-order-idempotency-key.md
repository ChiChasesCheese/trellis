---
id: hi-pt-book-seller-platform-5-order-idempotency-key
node: qb.sd.book-seller-platform.points
type: qa
step: 5
---
## Q
**图书比价代购平台 · 下单幂等键**｜出自：图书比价代购平台 › 深入 2

顾客在图书平台点了两次下单，或客户端网络重试，导致同一请求到达两次。接口层怎么保证不会触发第二次购买？

## A
**要点。** 请求头带 Idempotency-Key，在订单库里 INSERT ... ON CONFLICT，重复请求返回同一订单，不再触发购买。
**边界。** 同一顾客对同一种书短时间内用两个不同的键下单，属于业务策略（提示或限制），不是技术保证。
**易错。** 以为幂等键能防住"用户有意再买一本"。
