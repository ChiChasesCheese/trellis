---
nodes: [problems.components.notification-service]
url: https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier1-foundation/003-notification-system
---
# machine-coding-interview-questions — Notification System

值得读：它把这道题定位成"观察者模式的练习"，README 里的 Before You Code 一节把出发点讲得很好
——下单系统不该 import 邮件服务，publisher 不认识 subscriber。附五种语言的骨架、分 part 递进的
要求，以及它标注的公司（Flipkart、Swiggy）和 45 分钟时限，可作节奏参考。分歧在建模：它让每个
渠道做 observer、事件来了逐个 `update()`，于是偏好判断散落在每个 observer 内部，而且没有地方
安放队列、优先级与用户级限额；本题解把偏好收进一个 `decide()`，把投递收进一条分道队列，
渠道退回成只有 `channel` 和 `send` 的策略对象。
