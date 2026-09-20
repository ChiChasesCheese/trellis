---
id: problems-atm-note-selection-no-chain
node: problems.machines.atm
type: qa
step: 7
tags: [grown]
---
## Q
ATM 的选钞（从钞箱现有面额里凑出金额）常被写成责任链（Chain of Responsibility）：一个处理器管一种面额，余额往下传。这个结构有什么问题？换成什么？

## A
两个问题，第二个致命。其一，四种面额写四个类加一个基类，换来的只是一个 `for note in sorted(available, reverse=True)` 循环，在 Python 里是纯仪式。其二，**链的形状把贪心焊死在结构里**：链就是从大到小依次决定，而这正是贪心；想换更聪明的算法得把整条链拆掉。正确形态是一个可替换的纯函数 `Callable[[int, Mapping[Note, int]], dict | None]`，默认实现用有界背包 DP，目标是张数最少（张数越多卡钞概率越高，且有送钞上限）。DP 的格子数先除以面额的最大公约数，取 2000 元也只有两百格，代价完全付得起。
