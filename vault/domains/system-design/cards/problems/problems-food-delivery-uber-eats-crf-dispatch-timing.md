---
id: problems-food-delivery-uber-eats-crf-dispatch-timing
node: problems.geo.food-delivery
type: qa
step: 6
tags: [grown]
---
## Q
Beyond deciding which courier to assign to which order, Uber Eats' engineering blog describes a second dispatch-timing problem: figuring out exactly when to send a courier to a restaurant. How does the system infer this timing, and why does it matter for delivery quality?

## A
The system fuses a courier's phone GPS with accelerometer and gyroscope readings and the Android Activity Recognition API to infer which of five trip states the courier is currently in (arrived at restaurant, parked, waiting at restaurant, walking to car, en route to eater), and uses a Conditional Random Field (CRF) to detect the moments when the courier transitions between these states from noisy sensor data. The goal is to time each courier's dispatch so they arrive at the restaurant just as the food finishes preparing, using the restaurant's historical prep-time patterns — dispatching too early leaves the courier waiting idle, while dispatching too late leaves food sitting and cooling before pickup, so this timing decision is a separate problem from matching, not something that comes for free once a courier is assigned.

## Q zh
除了决定把哪个订单指派给哪个骑手之外，Uber Eats 的工程博客还描述了另一个调度时机问题：准确判断什么时候该派骑手去商户取餐。系统是如何推断这个时机的？为什么它对配送质量很重要？

## A zh
系统把骑手手机的 GPS 和加速度计、陀螺仪读数，以及 Android 的活动识别 API 融合起来，推断骑手当前处于五种行程状态中的哪一种（已到店、停车中、在店内等待、走向车辆、前往顾客），并用条件随机场（Conditional Random Field, CRF）从带噪声的传感器数据里识别骑手在这些状态之间切换的时间点。目标是利用商户的历史备餐时长模式，让骑手恰好在餐做好的那一刻到店——派得太早会让骑手空等，派得太晚会让餐在后厨放凉才被取走，所以这个时机决策是一个独立于匹配本身的问题，不是指派好骑手之后自动就解决的。
