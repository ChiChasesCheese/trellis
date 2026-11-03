---
id: hi-pt-tt-flash-sale-ticketing-5-redis-gate
node: tt.sd.tt-flash-sale-ticketing.points
type: qa
step: 5
---
## Q
**秒杀抢票 · Redis 闸门加数据库真相**｜必会 · 出自：秒杀抢票 › 深入 2

秒杀抢票的库存扣减，数据库行锁、只用 Redis DECR、单消费者队列、Redis 闸门加数据库真相各有什么问题？

## A
**行锁。** 正确，但单行 500/s。**只用 Redis DECR。** 快，但故障转移丢扣减，无持久真相。**单消费者。** 正确但延迟高。
**选用。** Redis 脚本一次完成限购检查、库存检查、扣减、登记占位；数据库 UPDATE inventory SET sold = sold + 1 WHERE sold < total 做最后一道，订单表两个唯一索引兜底。
**保证。** sold <= total 由数据库保证，与 Redis 状态无关。
