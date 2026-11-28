---
id: hi-c-sd-notification-system-x11-ha-cron
node: sd.problem-breakdowns.notification-system.exam
type: qa
step: 11
---
## Q
**通知系统 · 预测：为 cron 做高可用起两个实例会怎样**｜考点 · 必会

定时发送由每分钟一次的 cron 扫描 SCHEDULED 行。为避免单点，起了两个 cron 实例，各自扫描并发布。会发生什么？有哪几种修法？

## A
- **后果：** 两个实例在同一分钟扫到同一批到期的行，各发布一遍，每条定时通知入队两次，用户收到重复。
- **修法一，认领行：** 用 `SELECT ... FOR UPDATE SKIP LOCKED` 或带条件的更新（把状态从 SCHEDULED 改为 DISPATCHING，成功的实例才发布），一行只被一个实例处理。
- **修法二，单领导者：** 通过租约选出一个实例运行，其他待命；领导者挂了租约过期后接手。要注意旧领导者可能"假死后复活"，需要围栏令牌（fencing token）。
- **修法三，靠下游去重兜底：** 通知 ID 由行 ID 确定性派生，两个实例发布的是相同 ID，下游的去重挡下第二份。这是兜底，不应作为主要手段，因为会白白增加队列流量。
- **加分：** 认领后实例崩溃，状态停在 DISPATCHING，需要超时回收机制，否则这些通知永远不发。
