---
id: hl-javaq-g-q37-main
node: java-questions.g-os
type: qa
step: 11
---
## Q
怎么对 JVM 做 profiling 和诊断？JFR、`jcmd`、线程转储、堆直方图，各看什么？
How do you profile and diagnose a JVM: JFR, `jcmd`, thread dumps, heap histograms? Show me what you would look at.

## A
一句话：JDK 自带的就够用：
- `jcmd <pid> Thread.print`：线程栈与锁。
- `jstat -gcutil <pid> 500`：GC 概况。
- `jcmd <pid> GC.class_histogram`：谁占堆（实例数 + 字节数）。
- `jcmd <pid> VM.native_memory`：堆外（需 NMT）。
- **JFR**（Java Flight Recorder，低开销事件录制）：CPU 采样、分配、锁、GC。
- 第三方：async-profiler（基于 `perf_events` + `AsyncGetCallTrace`，不受 safepoint 偏差影响）、VisualVM。
- 注意：线程转储本身会进 safepoint，密集反复采集会引入停顿。
