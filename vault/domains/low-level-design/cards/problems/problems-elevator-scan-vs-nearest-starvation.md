---
id: problems-elevator-scan-vs-nearest-starvation
node: problems.machines.elevator
type: qa
step: 4
tags: [grown]
---
## Q
电梯选下一站时，“永远去最近的那个请求”（nearest-request）和经典电梯算法（SCAN／LOOK：朝一个方向一路服务到底再掉头）相比差在哪里？请说出具体的失败场景。

## A
差在有没有等待上界。nearest-request 是贪心的，只要近处一直有人按，它就在近处来回摆动，20 楼的请求可以永远排不上——这是饥饿（starvation），不是“慢一点”。SCAN 的公平性来自“一趟扫描最多一个来回”：任何请求最迟在电梯扫到它所在那一段时被服务，等待时间有明确上界。面试里说“我用了电梯算法”只是报了个名字，说出“它保证任何请求在一个来回内被服务”才算答上。
