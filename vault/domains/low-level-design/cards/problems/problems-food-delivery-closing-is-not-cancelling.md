---
id: problems-food-delivery-closing-is-not-cancelling
node: problems.marketplaces.food-delivery
type: qa
step: 8
tags: [grown]
---
## Q
外卖平台上一家餐厅中途打烊，此刻它手上有已接单和未接单两种订单。各自该怎么处理？为什么这个需求不会动到派单代码？

## A
**关店不是撤单。** 餐厅接单那一刻就已经承诺了，菜也已经在做，所以：

- 已接的单（ACCEPTED）**照常做完、照常送**，派单逻辑毫不知情；
- 还没被接的单（PLACED，以及还没放出来的定时单）由**平台代为拒绝**（REJECTED，`by=PLATFORM`，reason 写明「餐厅打烊」）；
- 新单在下单时就被挡回（`RestaurantClosedError`）。

不动派单的原因很具体：派单只认 `ready_at`，而 `ready_at` 只在餐厅接单那一刻产生；被拒掉的单从来没有过 `ready_at`，本来就不在派单的候选集里。所以「打烊」只是**批量走一条已经存在的边**。

同一个道理适用于定时单：它多一个 SCHEDULED 状态和一条 `SCHEDULED → PLACED` 的出边，到点由平台放出来，之后和普通订单完全一样。老实说这里确实**加了**一个状态——说「完全没动」是不诚实的，说「只加不改」才是对的。
