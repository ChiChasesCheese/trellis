---
id: hi-c-lld-delivery-x02-entity-filter
node: lld.in-a-hurry.delivery.exam
type: qa
step: 2
---
## Q
**LLD 答题框架 · 判断哪些名词该做实体**｜考点 · 必会

"设计停车场，车辆进场时分配车位"。`Car`、`LicensePlate`、`Spot`、`Ticket`、`ParkingLot` 里，哪些应该是独立实体？

## A
- **用过滤规则：** 有会变的状态或要执行规则的才独立
- **`ParkingLot`：** 协调者，负责分配与释放流程
- **`Spot`：** 有"空闲/占用"状态和类型规则，独立
- **`Ticket`：** 记录入场时间与所占车位，随进出变化，独立
- **`LicensePlate`：** 只是车辆的信息，作为 `Car` 的字段
- **`Car`：** 若只用于带车牌和类型进来，也可以只是入参里的值，别让它长出一堆行为
