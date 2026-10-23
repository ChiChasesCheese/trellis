---
id: hl-sdrun-java-floor
node: system-design.how-to-run
type: qa
step: 28
---
## Q
Java 做交易热路径的诚实下限在哪？很多公司把 Java 用在哪里？

## A
规范写出来的 Java 热路径可以做到个位数到几十 µs 的 tick-to-trade；要进入亚微秒，通常是 C++ / FPGA 的领地。

所以很多公司把 Java 用在**研究平台、风控监控、编排、对账**这些「慢侧」，热路径用 C++。面试里承认这一点比硬吹 Java 无所不能更可信。
