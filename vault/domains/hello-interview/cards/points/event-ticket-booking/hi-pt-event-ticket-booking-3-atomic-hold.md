---
id: hi-pt-event-ticket-booking-3-atomic-hold
node: qb.lld.event-ticket-booking.points
type: qa
step: 3
---
## Q
**活动票务预订后端 · 原子占库存**｜出自：活动票务预订后端 › 深入 1

活动票务开售瞬间数万人抢同一票型。代码里检查余量和占住库存应该怎么写，才不会两个请求同时看到"还剩 1 张"？

## A
**要点。** 检查与占住在同一个原子步骤里完成；内存版用锁，数据库版用一条条件 UPDATE：
```python
# UPDATE ticket_type SET held = held + :qty
# WHERE id=:id AND now() BETWEEN sale_start AND sale_end
#   AND total - sold - held >= :qty;
```
**判定。** 受影响行数为 0 就是售罄或未开售，为 1 才插入 reservation，且在同一事务内。
