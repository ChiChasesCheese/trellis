---
id: hl-javaq-g-q37-say60
node: java-questions.g-os
type: qa
step: 17
---
## Q
用英文 60 秒回答：How do you profile and diagnose a JVM: JFR, `jcmd`, thread dumps, heap histograms? Show me what you would look at.

## A
结构：线程转储看状态与锁 → jstat 与类直方图看 GC 和堆 → JFR 看 CPU 热点（实测 fib 占 79%）→ NMT 看堆外 → JFR 开销低可常开，async-profiler 用于精确的原生与 JIT 帧。

> "For a live JVM I start with `jcmd Thread.print` - it shows thread states and which monitor each thread holds or waits for, so contention and deadlocks are visible immediately. `jstat -gcutil` shows GC frequency and time, and `GC.class_histogram` shows what's filling the heap. For CPU I use Java Flight Recorder: start it with a flag or `jcmd JFR.start`, then `jfr view hot-methods` - on a test JVM it identified the recursive function at 79% of samples. For native memory, native memory tracking with `VM.native_memory`. JFR is low overhead enough to leave on in production, and async-profiler is the usual choice when I need accurate native and JIT frames."
