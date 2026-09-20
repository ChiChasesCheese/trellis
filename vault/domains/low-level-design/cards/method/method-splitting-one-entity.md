---
id: method-splitting-one-entity
node: method.modeling
type: qa
step: 5
---
## Q
什么信号说明模型里的一个类其实是两个实体，该怎么具体重构？

## A
最强的信号是字段的生命周期不同：`shipped_at`、`carrier`、`tracking_id` 在 `Order` 的大部分生命周期里都是 `None`——只在某个阶段之后才有值的字段，通常是藏在里面的第二个对象。另一个信号是基数以后会不同：一旦"一个订单可以拆成多个包裹发货"，这些字段就要变成列表，拆分已经是必然的了。

具体重构：把这组"直到某阶段才有值"的字段收进一个嵌套的 `Shipment` 对象，`Order` 上只留一个可能为 `None` 的 `shipment` 字段。
