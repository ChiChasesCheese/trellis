---
id: structure-api-rich-return-contract
node: structure.api
type: qa
step: 1
---
## Q
停车场（parking lot）机考题：`park(vehicle)` 该返回 `bool` 还是一个 `Ticket` 对象？面试官接下来大概率会追加"出口要按停车时长收费"，哪种设计能扛住？

## A
返回 `Ticket`（一个携带入场时间、车位号、车辆信息的领域对象）能扛住。`unpark(ticket)` 后续可以直接从 `ticket` 里算出费用、定位车位、做校验，不需要改任何已有方法签名；新需求只是往 `Ticket` 上加**字段**。返回裸 `bool` 的设计每来一个新需求都要改签名——调用方还是只拿到"成功与否"，什么都算不出来。

通用规则：让返回值是一个**命名了这次交互**的领域对象（`Ticket`、`Booking`、`Receipt`），不要用一个裸的成功标志替代它。
