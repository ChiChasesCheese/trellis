---
id: problems-restaurant-served-total-is-query
node: problems.booking.restaurant
type: qa
step: 3
tags: [grown]
---
## Q
餐厅管理设计里，`Order.served_total`（账单金额）为什么是对每一行菜当前状态的一次实时查询，而不是下单时就锁定、之后累加扣减的一个字段？

## A
把总额写成一个被写入的字段，会在三种情况下崩掉：一道菜缺货了，总账要不要减；顾客先付了一半又点了甜点，总额该是原来的数字还是要重算；一道还在锅里没上桌的菜凭什么已经算进了要平摊的钱里。把 `served_total` 定义成“只统计状态为 SERVED 的行”，三个问题一次性解决：缺货的行状态是 UNAVAILABLE，天然不计入账单；`balance_due = served_total - paid_total`，新菜一旦上桌，账单自动重新变大——“先付一部分、再加菜”不需要任何专门设计的状态或分支，是账单永远现算这条设计的自然推论。
