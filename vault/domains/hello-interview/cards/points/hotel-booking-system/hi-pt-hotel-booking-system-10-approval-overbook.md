---
id: hi-pt-hotel-booking-system-10-approval-overbook
node: qb.sd.hotel-booking-system.points
type: qa
step: 10
---
## Q
**酒店预订系统 · 酒店审批与超额预订**｜出自：酒店预订系统 › 取舍与追问

追问：酒店需要审批预订怎么处理？酒店业的主动超订怎么支持？

## A
**审批。** 预订进入 PENDING_SUPPLIER，保留库存并设较长期限；酒店通过 webhook 确认或拒绝，超时自动取消；取消事件带事件 ID，幂等处理后把库存加回。
**超订。** 条件改为 `reserved < total * (1 + ratio)`，作为产品配置，不改事务逻辑。
