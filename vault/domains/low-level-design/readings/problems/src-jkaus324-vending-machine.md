---
nodes: [problems.machines.vending-machine]
url: https://github.com/jkaus324/machine-coding-interview-questions/tree/main/problems/tier1-foundation/004-vending-machine
tags: [no-archive]
---
# machine-coding-interview-questions — 004 Vending Machine

值得读：它把这道题的核心问题提得最直白——"转移逻辑到底放在哪"，并且按基础／进阶分关列出
要求，节奏和真实机器编码轮一致，适合用来核对自己的分关有没有漏项（状态转移、库存、找零、
补货）。它的结论是"用 State 模式，每个状态一个类，这样加状态不用改已有方法"。本题解给出的
是一条带条件的答案：判据不是状态多不多，而是每个状态有没有自己成套的进入／退出副作用；
在只有四个状态、动作各自只有几行的规模下，转移表更短，而且能被一个穷举测试盖满。
（仓库无 LICENSE，只链接不复制。）
