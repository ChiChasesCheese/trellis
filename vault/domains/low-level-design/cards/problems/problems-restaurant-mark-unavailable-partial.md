---
id: problems-restaurant-mark-unavailable-partial
node: problems.booking.restaurant
type: qa
step: 7
tags: [grown]
---
## Q
餐厅管理设计里，后厨中途宣布一道菜没货了，已经点了这道菜、且已经开始在做的那几份会怎么样，为什么不是整单都失败？

## A
已经在做（PREPARING）或已经做好（READY/SERVED）的那几份不受影响，继续走完它们的状态机；只有还在排队、状态还是 ORDERED 的同款菜品行，会被转移到 UNAVAILABLE 这个终态，并从后厨的排队队列里移除。理由是：后厨用完了食材，不代表已经下锅的那份也没了原料，把已经在锅里的菜也撤掉是把库存问题错误地传导成了服务问题；这道菜之后再被点，`Kitchen.submit` 的校验会直接拒绝，防止顾客点了一道永远做不出来的菜。
