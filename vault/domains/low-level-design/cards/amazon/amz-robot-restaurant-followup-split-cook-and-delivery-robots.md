---
id: amz-robot-restaurant-followup-split-cook-and-delivery-robots
node: amazon.amz-robot-restaurant
type: qa
step: 6
tags: [grown]
---
## Q
在 Amazon 机器人餐厅设计里，若追问「做菜机器人和送餐机器人分开」（推断的追问），哪里要改、哪里不动？

## A
改：订单阶段拆成「等厨师」「等送餐」两个队列；`Robot` 增加 `role`；`_dispatch` 按阶段选队列和角色匹配的候选；做完菜的订单放进送餐队列。不动：机器人状态机与转移表、`Config`、策略函数签名、`Order`、`Dish`。能这么改，是因为状态机与「谁派给谁」本来就是分开的。
