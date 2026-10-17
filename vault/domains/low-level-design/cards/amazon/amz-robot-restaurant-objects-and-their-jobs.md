---
id: amz-robot-restaurant-objects-and-their-jobs
node: amazon.amz-robot-restaurant
type: qa
step: 2
tags: [grown]
---
## Q
在 Amazon 机器人餐厅设计里，应有哪几个对象？各自只负责什么？

## A
`Order`：订单记录（桌号、菜、状态），无行为。`Robot`：拥有状态、电量、手上订单，每刻 `step()` 一次，是状态机的唯一执行者。`RobotView`：机器人的只读快照，策略只能看它。`AssignmentPolicy`：选哪台机器人接单的函数。`Restaurant`：收单、排队、推进时间、派单，并持有锁。切分依据：变化原因各不相同。
