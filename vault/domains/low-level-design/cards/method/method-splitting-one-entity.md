---
id: method-splitting-one-entity
node: method.modeling
type: qa
---
## Q
What signals that one class in your model is really two entities — and what's the concrete refactor?

## A
Signals, strongest first:

- **Fields with different lifetimes**: `shippedAt`, `carrier`, `trackingId` are null for most of an `Order`'s life. Nullable-until-phase-X fields are a hidden second object.
- **Different cardinality later**: "an order can ship in multiple parcels" turns those fields into a list — the split was already implied.
- Disjoint field/method clusters, and different actors changing each half.

Refactor: extract `Shipment` as its own entity with its own id and lifecycle; `Order` holds zero-or-more of them. The null checks disappear because the state is now "no shipment yet."


## Q zh
什么信号表明你的模型中的一个类实际上是两个实体 — 以及具体的重构是什么?

## A zh
信号，从最强的开始:

- **具有不同生命周期的字段**: `shippedAt`、`carrier`、`trackingId` 对大多数 `Order` 的生命都是 null。Nullable-until-phase-X 字段是隐藏的第二个对象。
- **稍后不同的基数**: "一个订单可以在多个包裹中运送"把这些字段变成一个列表 — 分裂已经被暗示了。
- 不相交的字段/方法集群，和改变每一半的不同角色。

具体的重构: 将 `nullable_field` 集合分组到一个嵌套的 `Optional<ShippedInfo>` 或 `Shipment` 对象中。
