---
id: hl-sd03-fu-prove-p9999
node: system-design.sd03-low-latency-trading
type: qa
step: 45
---
## Q
追问：怎么测量并证明 p99.99？协调遗漏是什么？

## A
线缆上测（tap + 硬件时间戳），不只是应用内；分段直方图（HdrHistogram 思想）；固定速率发送器，按「应发送时间」计延迟避免协调遗漏；分位数不能相加，必须端到端测；延迟-时间图找周期性毛刺的共同原因（GC、刷盘、THP、中断）；1M msg/s 时 p99.99 意味着每秒 100 条超标，所以要看 p99.99 之后的 max 与持续时间。

可以说：「我不信应用里的 `nanoTime`，我信线缆上的时间戳。」
