---
id: problems-vending-machine-table-vs-state-classes
node: problems.machines.vending-machine
type: qa
step: 1
tags: [grown]
---
## Q
自动售货机（Vending Machine）有 IDLE / COIN_INSERTED / DISPENSING / RETURNING_CHANGE 四个状态和投币／选货／出货／取找零／退币五个动作。用 `Enum` 加一张 `dict[(状态, 动作), 新状态]` 转移表，和一状态一个类（State 模式），该选哪个？

## A
在这个规模下选转移表。4 × 5 = 20 个组合里只有 6 个合法，一状态一类意味着把同一句“这个动作现在不行”抄十四遍，而且漏重写一个方法没有任何地方查得出来——基类的默认实现会把本该拒绝的动作悄悄放行。转移表把合法性变成一份只有六行的数据，于是可以写一个穷举测试：遍历全部 20 个组合，凡是不在表里的都断言抛非法转移异常。翻到 State 类的判据不是“状态多不多”，而是每个状态有没有成套的进入／退出副作用（进入出货要启动电机、点灯、起超时定时器，离开要逐个收尾）；只是“这个动作能不能做”时，表更短也更可验证。
