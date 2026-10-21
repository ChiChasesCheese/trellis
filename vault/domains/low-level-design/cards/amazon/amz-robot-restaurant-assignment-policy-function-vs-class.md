---
id: amz-robot-restaurant-assignment-policy-function-vs-class
node: amazon.amz-robot-restaurant
type: qa
step: 5
tags: [grown]
---
## Q
在 Amazon 机器人餐厅设计里，「哪台空闲机器人接这张单」怎么做成可替换的？为什么策略拿到的是快照而不是机器人本身？

## A
策略就是一个函数 `(candidates: Sequence[RobotView], dish) -> int | None`，`first_idle`、`most_battery` 各三行；只有一个方法的类是 Java 习惯。候选交快照（frozen dataclass），策略只能选、不能改机器人。餐厅收到编号后校验它在候选里，否则抛 `PolicyError`——写错的策略不能把单派给正在送餐的机器人。
