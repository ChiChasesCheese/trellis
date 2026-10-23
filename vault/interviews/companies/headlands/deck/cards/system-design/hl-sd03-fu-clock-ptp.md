---
id: hl-sd03-fu-clock-ptp
node: system-design.sd03-low-latency-trading
type: qa
step: 46
---
## Q
追问：时间戳从哪来？PTP 失步会怎样？

## A
网卡硬件时间戳 + PTP / GPS 同步，精度远优于 NTP；业务时间用事件里的时间戳（决定性）；监控偏移，失步 ⟹ 告警，对账与延迟度量降级（交易功能不应依赖绝对时间，只依赖单调与序号）；`System.nanoTime()` 只用于相对延迟。

可以说：「决定性要求时间是输入，不是环境。」
