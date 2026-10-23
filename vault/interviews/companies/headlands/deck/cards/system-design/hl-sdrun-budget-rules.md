---
id: hl-sdrun-budget-rules
node: system-design.how-to-run
type: qa
step: 19
---
## Q
使用延迟预算的规则有哪些？为什么报分位数而不是平均？什么是逆向选择（adverse selection）？

## A
1. 每一段**有人认领**（线程 / 组件）、有**测量点**（硬件时间戳或单调时钟）；
2. 报**分位数**：p50 / p99 / p99.99 / max，不是平均。一次 2 ms 的 GC 停顿里，行情继续跑，你的报价已经陈旧；陈旧报价会被更快的对手吃掉，这叫**逆向选择**：成交的恰好都是对你不利的单；
3. 测量避免**协调遗漏（coordinated omission）**：压测器在被测系统卡住时停止发送就把最差延迟藏起来了。用固定速率发送器 + 记录「应该发出」的时间，用 HdrHistogram 一类直方图；
4. 把 OS 配置当作设计的一部分：`isolcpus` / `nohz_full` 隔离核心、`taskset` 绑核、关闭 `irqbalance`、`performance` 调频策略、大页、NUMA 就近分配、关闭 swap。
