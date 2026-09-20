---
id: problems-restaurant-atomic-submit-rollback
node: problems.booking.restaurant
type: qa
step: 8
tags: [grown]
---
## Q
餐厅管理设计里，一次性点了三道菜，其中一道此刻缺货，`RestaurantService.submit_items` 最终会在这张点单上留下几道菜的记录，是怎么做到的？

## A
零道——缺货会让这次提交整批失败，点单上不会留下另外两道本来能做的菜。做法是：先把三行都加进 `Order`，再调用 `Kitchen.submit` 做“校验有没有货、通过就一次性入队”这两步，两步在后厨自己的锁里连续完成，不留检查和入队之间的时间缝；如果后厨因为缺货抛出异常，`RestaurantService` 会用 `Order.discard_line` 把刚加进去的三行全部撤回，点单恢复成提交前的样子。这样账本上不会出现“已经在点单里、但后厨根本不知道”的幽灵行。
