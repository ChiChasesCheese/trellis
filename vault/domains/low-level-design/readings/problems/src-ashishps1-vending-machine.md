---
nodes: [problems.machines.vending-machine]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/vending-machine.md
---
# awesome-low-level-design — Vending Machine

值得读：六种语言（含 Python）并排给出同一份设计，`VendingMachineState` 接口加
`IdleState` / `ReadyState` / `DispenseState` 三个状态类，`VendingMachine` 写成 Singleton。
它是本题解的主要参照系：本文要说明为什么在 Python 里 Singleton 不必要（测试必须能同时造两台
互不干扰的机器），以及在四个状态、五个动作的规模下，一张转移表为什么比一状态一类更容易被
测试盖满——它的状态类里绝大多数方法体都是"抛异常"，而漏重写一个方法没有任何地方查得出来。
它对"找不开零钱该怎么办"着墨很少，那恰是本文花最多篇幅的地方。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/vending-machine.md)
%% trellis:end %%
