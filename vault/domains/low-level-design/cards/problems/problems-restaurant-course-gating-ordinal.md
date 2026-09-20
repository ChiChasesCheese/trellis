---
id: problems-restaurant-course-gating-ordinal
node: problems.booking.restaurant
type: qa
step: 6
tags: [grown]
---
## Q
餐厅管理设计里，“开胃菜必须先于主菜就绪”这条课程顺序规则，为什么用课程的序数值比较（`sib.course.value < line.course.value`）来实现，而不是写一个 `if line.course == MAIN and not all_starters_ready` 的特判？

## A
特判只对两道课程成立，题目一旦有第三道课程（甜点），就要再加一条 `if`，而且两条分支之间的一致性没人保证。本文把课程建模成一个有大小关系的序数（STARTER=1 < MAIN=2 < DESSERT=3），门禁规则只有一条：某道菜能开始做，当且仅当同一单里课程序号更小的兄弟菜都已经就绪或到了终态。这一条规则同时管住了任意多道课程之间的先后关系，加多少道课程都不用改 `Kitchen` 的代码，只需要在 `Course` 里多加一个枚举成员——把“两两特判”抽象成“偏序关系”。
