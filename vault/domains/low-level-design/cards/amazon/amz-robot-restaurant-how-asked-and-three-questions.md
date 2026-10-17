---
id: amz-robot-restaurant-how-asked-and-three-questions
node: amazon.amz-robot-restaurant
type: qa
step: 1
tags: [grown]
---
## Q
机器人餐厅（Robot Restaurant）要你设计什么？开场先问哪三个澄清问题？

## A
要设计的是一间由机器人送餐的餐厅：顾客点单，空闲的机器人接单、做菜、送到桌子，然后回到空闲；机器人有电量，低了要去充电桩。题面只有一个名字，细节要自己问。三问：(1) 一台机器人是否做菜送餐一条龙——决定状态机与订单阶段是否一一对应；(2) 时间用真实时钟还是离散的刻（tick）——决定能否测试；(3) 分配规则与电量不足怎么办——决定策略要不要可换、要不要加充电状态。
