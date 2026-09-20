---
nodes: [problems.machines.elevator]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/elevator-system.md
---
# awesome-low-level-design — Elevator System

值得读：Java / Python / C++ / C# / Go 五种语言并排给出同一份设计，类是 `ElevatorSystem` /
`ElevatorController` / `Elevator` / `Request`，方向枚举只有 UP / DOWN，派梯规则是"离得最近
的那部梯"，并给每部梯开一个线程处理请求。它正是本题解的参照系：本文要说明"最近"作为派梯
规则会把外呼交给一部正在反方向跑的梯，作为单梯停靠规则会饿死远处楼层；线程加 sleep 则让
整道题失去确定性测试的可能——本文改用 tick 加注入时钟。
