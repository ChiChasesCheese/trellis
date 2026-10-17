---
id: amz-occupancy-tracker-how-asked-and-three-questions
node: amazon.amz-occupancy-tracker
type: qa
step: 1
tags: [grown]
---
## Q
办公室人数追踪（Occupancy Tracker）要你设计什么？开场先问哪三个澄清问题？

## A
要设计的是根据刷卡进出事件回答「任意时刻楼里有多少人」的系统，后面还会问某段时间内的最大人数。三个问题，每个答案都改变设计：(1) 只问现在，还是要问任意历史时刻——要问历史，就必须存事件而不是存人数；(2) 事件是否按时间顺序到达、同一秒内谁先谁后——顺序到达才能只追加；(3) 有几个楼层或楼栋——决定要不要每个区域一条时间线。
