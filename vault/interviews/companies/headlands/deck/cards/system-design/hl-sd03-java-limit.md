---
id: hl-sd03-java-limit
node: system-design.sd03-low-latency-trading
type: qa
step: 29
---
## Q
Java 做交易热路径的诚实上限是什么？更合理的分工是什么？

## A
规范写出来的 Java 热路径通常能做到**个位数到几十 µs** 的 tick-to-trade；要进入亚微秒，通常是 C++ 或 FPGA 的领地（行业经验判断）。

更合理的分工：**C++ / FPGA 做最短的报价–撤单环；Java 做策略编排、风控监控、对账、研究回放、日志基础设施**。这与 Java 岗偏研究平台 / 存储 / 监控、C++ 岗偏 exchange connectivity、lock-free、profiling 的分工一致。

即使是 Java 不在最短路径上的岗位，**懂这些原理**也是被考的内容：面试官看重对计算机整条技术栈细节的掌握。
