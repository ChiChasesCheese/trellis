---
id: hl-bs-s5-hook
node: behavioral.stories
type: qa
step: 23
---
## Q
数据源切换故事 S5 的钩子句是什么？用来回答哪些问题？有哪些数字、哪两个百分比不能混？

## A
钩子："**I validated with the production query itself, so there was no gap between what I tested and what I shipped.**"

用于：**how do you test a risky change**、**a performance decision**、**ship fast safely**、**biggest system change**。

数字：字段级一致率 **>99.9%**；不一致的 **0.07%** 全是"单侧当日才有"的记录（时序，不是冲突）。切换前跑生产查询的 `count(*)`：**13,737,670 vs 13,768,430**，差 **+0.224%**。**0.07% 和 0.224% 是两个不同的数**。简历口径：**13.7M 行**切换。
