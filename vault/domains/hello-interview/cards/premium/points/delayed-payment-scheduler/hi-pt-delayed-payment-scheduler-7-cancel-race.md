---
id: hi-pt-delayed-payment-scheduler-7-cancel-race
node: qb.sd.delayed-payment-scheduler.points
type: qa
step: 7
---
## Q
**延迟支付调度服务 · 取消与执行的竞争**｜必会 · 出自：延迟支付调度服务 › 深入 3

付款人点取消的同时，扫描器正好抢占了这条到期预约。怎样保证只有一方生效，不会既退款又转账？

## A
**要点。** 都用条件更新决胜。取消：`UPDATE ... SET status='CANCELLED' WHERE id=? AND status='SCHEDULED'`，同一事务写 RELEASE 分录并加回余额；抢占语句也要求 `status='SCHEDULED'`。

两者对同一行互斥，要么取消赢要么执行赢。取消影响 0 行，说明已被抢占或完成，返回 409。
