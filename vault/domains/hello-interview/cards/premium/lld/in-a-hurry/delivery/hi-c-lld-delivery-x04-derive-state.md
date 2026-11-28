---
id: hi-c-lld-delivery-x04-derive-state
node: lld.in-a-hurry.delivery.exam
type: qa
step: 4
---
## Q
**LLD 答题框架 · 从需求推状态与行为**｜考点 · 必会

需求是"咖啡机能做咖啡和意式浓缩，原料不足时拒绝，出品后扣减原料"。`CoffeeMachine` 需要记住什么、暴露什么方法？

## A
| 需求 | 状态 | 行为 |
|---|---|---|
| 做两种饮品 | 饮品配方表 | `make(drink)` |
| 原料不足拒绝 | 各原料库存 | 内部检查库存 |
| 出品后扣减 | 同上 | `make` 成功后扣减 |

- **查询：** 需要时提供 `stock()`；其余不外露
- **规则归属：** 库存是否够，由持有库存的类自己回答
