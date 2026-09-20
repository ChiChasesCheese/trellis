---
nodes: [problems.marketplaces.ride-sharing]
url: https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier2-intermediate/021-ride-sharing
tags: [no-archive]
---
# machine-coding-interview-questions — 021 Ride-Sharing Application

值得读：它把题目按"基础要求 / 扩展 1 / 扩展 2"分关列出并附输入输出样例，节奏和真实机器编码轮
一致，最适合拿来检查自己的分关拆得全不全；每题前面的 "Before You Code" 会先写出朴素解法
（一串 `if-else` 的 `selectRide`）再解释它为什么会烂掉，这个"先给反例"的讲法很值得学。
它对本题的理解是**顺风车**：车主发布一趟行程，乘客用可插拔的策略（偏好车型、空座最多）去挑，
因此它的 Strategy 落在"乘客怎么挑车"上，和本题解的"系统怎么找人"恰好是镜像的两半——两者都
成立，但只有后者需要面对独占、超时与拒单。它几乎不涉及并发，也没有显式的行程状态机，
状态只是 `Ride` 上的一个 `active` 布尔值。实现是五种语言的同一份设计。（仓库无 LICENSE，
只链接不复制。）
