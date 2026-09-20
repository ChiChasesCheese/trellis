---
id: problems-meeting-scheduler-no-strategy-class-for-room-pick
node: problems.booking.meeting-scheduler
type: qa
step: 4
tags: [grown]
---
## Q
会议室预订设计里，“挑一间满足条件的最小房间”为什么不用策略模式（Strategy）——建一个选房接口、再配几个只有一个方法的实现类？

## A
“挑满足条件里最小的那个”就是一次按容量排序、加一次线性扫描找第一个满足条件（人数、设备、此刻空闲）的房间，逻辑本身很薄，不值得为它单独建一层类。如果确实需要多种可插拔的配房规则，Python 的做法是注入一个普通函数，而不是像常见的 Java 参照实现那样为每种规则建一个只有一个方法的类——本题目前只有一种配房逻辑，连注入点都不该在只有一种实现时就预先开出来。
