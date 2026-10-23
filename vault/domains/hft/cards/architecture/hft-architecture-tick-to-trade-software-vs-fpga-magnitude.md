---
id: hft-architecture-tick-to-trade-software-vs-fpga-magnitude
node: architecture.tick-to-trade
type: qa
step: 2
---
## Q
软件实现的交易系统和 FPGA 实现的交易系统，tick-to-trade 延迟大约各是什么量级？差别来自哪里？

## A
大致量级（随年代、品种、策略而变）：
- 纯软件（C++ 或 Java，配合内核旁路）：约**几微秒到几十微秒**。
- FPGA（可编程硬件电路）：约**几十到几百纳秒**。

差别的原因：软件要由 CPU 取指令、读内存（一次缓存未命中约 80–100 ns），还会受操作系统和垃圾回收等抖动影响；FPGA 把解码和判断做成硬件电路，数据按时钟周期流过。例如时钟每周期 4 ns，流水线 50 级也只有 200 ns，而且每次几乎一样，没有缓存未命中和调度。

代价是 FPGA 开发周期长、逻辑改动慢，所以通常只放最简单、最赶时间的那段逻辑。
