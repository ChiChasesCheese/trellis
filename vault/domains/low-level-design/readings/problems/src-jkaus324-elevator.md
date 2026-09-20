---
nodes: [problems.machines.elevator]
url: https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier2-intermediate/012-elevator-system
tags: [no-archive]
---
# machine-coding-interview-questions — 012 Elevator System

值得读：这个仓库把每道题按"基础要求 / 进阶要求"分关列出，节奏和真实的机器编码轮一致，
适合用来对照自己的分关拆得全不全（外呼与内选、调度策略、多梯派梯、检修与容量）。实现是
五种语言的同一份 Java 风格设计：`Request` 继承树加控制器单例。本题解在"核心对象与职责"
里说明了为什么在 Python 里这两样都不建——只有数据没有多态行为的继承树等于两个字段加一个
判断，而"全楼只有一组电梯"是业务事实，不是拦截构造的理由。（仓库无 LICENSE，只链接不复制。）
