---
id: hft-measurement-timestamps-clock-gettime-vdso
node: measurement.timestamps
type: qa
step: 2
---
## Q
Linux 的 `clock_gettime` 是系统调用，为什么只要约 20–30 ns？什么情况下它会变得很慢？它和 Java 的 `System.nanoTime()` 是什么关系？

## A
一般系统调用要进入内核，需要约几百纳秒到一微秒。`clock_gettime` 例外，因为有 **vDSO**（virtual dynamic shared object）：内核把一小段代码和时间数据映射进每个进程的地址空间，用户态直接读取，**不进内核**。它内部通常也是读 TSC 再换算，所以耗时约 20–30 ns，比裸 `rdtsc` 多一点，但已经带上了校准和换算。

会变慢的情形：当前时钟源（clocksource）不是 TSC，例如虚拟机或某些配置下退回到 `hpet`、`acpi_pm`，这些需要读设备寄存器或真正的系统调用，耗时升到微秒级，热路径上不可接受。检查办法：查看 `/sys/devices/system/clocksource/clocksource0/current_clocksource`，应为 `tsc`。

Java 的 `System.nanoTime()` 在 Linux 上基本就是 `clock_gettime(CLOCK_MONOTONIC)`，同样约 20–30 ns，所以它能用来做细粒度打点，但每次调用本身也有成本。
