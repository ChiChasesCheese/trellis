---
id: amz-robot-restaurant-how-asked-and-three-questions
node: amazon.amz-robot-restaurant
type: qa
step: 1
tags: [grown]
---
## Q
Amazon 面试里「机器人餐厅（Robot Restaurant）」是怎么问的？开场先问哪三个澄清问题？

## A
报告里只有题名：2026-09 一亩三分地的 SDE II 电面，三道题之一是「设计机器人餐厅」并有追问，题面细节不可见，其余都是重建。三问：(1) 一台机器人是否做菜送餐一条龙——决定状态机与订单阶段是否一一对应；(2) 时间用真实时钟还是离散的刻（tick）——决定能否测试；(3) 分配规则与电量不足怎么办——决定策略要不要可换、要不要加充电状态。
