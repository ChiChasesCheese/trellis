---
nodes: [problems.machines.elevator]
url: https://github.com/abhaypaswan/lld-python/tree/main/problems/elevator-system
---
# abhaypaswan/lld-python — Elevator System

值得读：整个题库里少见的纯 Python 解，而且和本题解一样把时间建模成 tick（"一拍走一层或
开一次门"）、明确把"派哪部梯"和"这部梯下一站去哪"拆成两个决定，还自带 pytest。核心类是
`ElevatorSystem` / `Elevator` / `SchedulingStrategy`，停靠请求用 `up_stops` / `down_stops`
两个集合。分歧点在于内选：它按"按下时的方向"并入其中一个集合，本题解额外分出 `car_calls`，
这样反方向经过时内选也会停，被停用的梯还能单独撤回外呼而不误伤车内乘客。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/abhaypaswan/lld-python/tree/main/problems/elevator-system)

## Archived copy
![[src-abhaypaswan-elevator-clip]]
%% trellis:end %%
