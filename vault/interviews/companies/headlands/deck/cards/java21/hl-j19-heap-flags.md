---
id: hl-j19-heap-flags
node: java21.j19-runtime-zgc-jit
type: qa
step: 9
---
## Q
低延迟 JVM 的堆参数 `-Xms`/`-Xmx`、`-XX:+AlwaysPreTouch`、`-XX:SoftMaxHeapSize` 分别做什么？为什么要设成这样？

## A
- `-Xms8g -Xmx8g`：初始堆 = 最大堆，避免运行时扩缩容；
- `-XX:+AlwaysPreTouch`：启动时就触碰所有堆页面，避免运行时才缺页；
- `-XX:SoftMaxHeapSize=...`：ZGC 的「软上限」，尽量不超过它，但需要时可超。

容器里的 JVM：内存限制、CPU 配额影响默认堆大小与 GC / JIT 编译线程数（`CICompilerCount`）。CPU 限额太小，JIT 与 GC 线程会和应用抢核。
