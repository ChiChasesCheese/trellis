---
id: hi-sd-ticketmaster-4-reserve-bad-good
node: sd.problem-breakdowns.ticketmaster
type: qa
step: 4
---
## Q
**预订座位：长事务锁与状态加定时清理**｜系统设计 · 问题拆解

为什么不能用 SELECT FOR UPDATE 长时间锁住票来做「结账倒计时」？状态加过期时间再用 cron 清理又有什么不足？

## A
**目标。** 用户结账时座位对别人锁定；放弃了要自动释放；付款成功要标为已售。

**差的方案：长时间数据库锁。** 在 PostgreSQL 里用 `SELECT FOR UPDATE` 锁行直到事务结束。问题：数据库锁是给瞬时事务用的，持有 5 分钟会消耗资源、增加争用与死锁风险，高负载下伸缩性差；崩溃或网络故障会让锁处于不确定状态；`lock_timeout` 只会让别人报错而不是排队，不适合面向用户的流程。

**较好的方案：状态加过期时间。** 票有 available / reserved / booked 三态，选座时置为 reserved 并记时间，cron 定期把过期的改回 available。

**不足。** 过期到清理之间有延迟，热门活动里票白白不可买；cron 出故障会让票一直不可用，造成收入损失。
