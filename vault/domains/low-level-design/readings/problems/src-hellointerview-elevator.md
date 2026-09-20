---
nodes: [problems.machines.elevator]
url: https://www.hellointerview.com/learn/low-level-design/problem-breakdowns/elevator
tags: [no-archive]
---
# Hello Interview — Low-Level Design: Elevator

值得读：商业课程的题目拆解，强项是把面试官的追问顺序整理得很清楚（先一部梯，再调度，
再多梯，再异常），可以拿来校准自己的分关节奏。它的代码走"一状态一类"的 State 形态，和本
题解选择的枚举加转移分支相反，正好拿来对照"状态数少、行为差异小就用枚举；每个状态都有成
套进入／退出副作用才升级成类"这条判据。付费站点，只链接不摘录。
