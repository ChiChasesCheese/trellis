---
id: hi-pt-tt-flash-sale-ticketing-7-idempotent-release
node: tt.sd.tt-flash-sale-ticketing.points
type: qa
step: 7
---
## Q
**秒杀抢票 · 占位释放幂等**｜必会 · 出自：秒杀抢票 › 深入 3

秒杀抢票的占位超时或付款失败要把票回补。怎样保证重复或并发释放只回补一次？

## A
**要点。** 只有 ZREM 真的删掉了成员，才 INCR stock 并 SREM bought。
**为什么。** 回补两次会让库存虚增，随后超卖。
**状态转移。** 数据库里每个转移是比较并交换：UPDATE hold SET state='paid' WHERE hold_id=? AND state IN ('held','ordered')，看影响行数。
