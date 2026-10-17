---
id: amz-pizza-order-objects-and-jobs
node: amazon.amz-pizza-order
type: qa
step: 2
tags: [grown]
---
## Q
在披萨订单设计里需要哪几个核心类？各自只负责什么？

## A
系统读顾客的选择和店里的优惠规则，产出一份校验过的披萨和一张订单账单。

- `Menu`：纯数据，尺寸、饼底、配料的价格、互斥表和配料上限。
- `PizzaBuilder`：分步收集选择，`build()` 时一次性校验，保证产出的每份披萨都合法。
- `Pizza`：不可变值对象，带构建时定格的单价；配料排序后，同样的披萨相等。
- `Order`：容器，同样的披萨合并成一行，对外只给快照。
- `LineRule` / `OrderRule` / `PriceEngine`：只看一行的优惠、看整单的优惠，以及遍历、钳位、记账的引擎。
