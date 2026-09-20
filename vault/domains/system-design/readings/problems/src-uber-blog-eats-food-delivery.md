---
nodes: [problems.geo.food-delivery]
url: https://www.uber.com/en-US/blog/uber-eats-trip-optimization/
---
# How Trip Inferences and Machine Learning Optimize Delivery Times on Uber Eats

值得读：Uber 官方工程博客，公开了 Uber Eats 调度里"什么时候派骑手去商户取餐"这个
时机问题的解法——融合 GPS、加速度计、陀螺仪和 Android 活动识别 API 的信号，推断骑手
处于到店/停车/店内等待/走向车辆/前往顾客五种状态中的哪一种，用条件随机场（CRF）识别
状态切换的时间点，目标是让骑手恰好在餐做好时到店。本题解「深入探讨」第 3 节用它来
补充 DoorDash 博客"谁指派给谁"这一层之外、"什么时候指派"这一层的论证，两篇原文的
侧重点不同，本题解把它们结合成一个更完整的调度论证。
