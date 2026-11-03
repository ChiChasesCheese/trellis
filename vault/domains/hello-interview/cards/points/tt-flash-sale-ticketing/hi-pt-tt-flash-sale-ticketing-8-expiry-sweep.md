---
id: hi-pt-tt-flash-sale-ticketing-8-expiry-sweep
node: tt.sd.tt-flash-sale-ticketing.points
type: qa
step: 8
---
## Q
**秒杀抢票 · 过期清扫与付款竞争**｜必会 · 出自：秒杀抢票 › 深入 3

秒杀抢票的占位 10 分钟过期。怎么做过期，第 9 分 59 秒付款成功与清扫同时发生怎么办？

## A
**过期。** 有序集合按过期时间排序，清扫任务每秒取 score ≤ now 的成员释放；不依赖 Redis 键过期通知，那是尽力而为会丢。
**竞争。** 两者都是对同一行的比较并交换，只有一个成功。付款先赢则变 paid；清扫先赢，迟到的付款回调发现已 released，此时钱已收：票还在恢复订单，不在自动退款。
