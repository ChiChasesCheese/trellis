---
id: hl-sd03-fu-java-floor
node: system-design.sd03-low-latency-trading
type: qa
step: 47
---
## Q
追问：如果 Java 的下限不够，你怎么办？

## A
承认；分工：最短的报价-撤单环用 C++ / FPGA，Java 做策略编排、风控监控、对账、研究回放、日志基础设施；用 FFM / 共享内存（SPSC 环）在 Java 与本地进程间传递事件；先测量再迁移，别凭感觉重写。

可以说：「我会先用测量告诉我 Java 的下限在哪，而不是预设它够不够。」
