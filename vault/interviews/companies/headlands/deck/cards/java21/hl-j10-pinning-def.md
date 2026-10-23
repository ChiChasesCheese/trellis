---
id: hl-j10-pinning-def
node: java21.j10-virtual-threads
type: qa
step: 17
---
## Q
什么是虚拟线程的 pinning（钉住）？JDK 21 里有哪两个主要原因，为什么会这样？

## A
**定义**：虚拟线程在**无法卸载**的状态下阻塞就叫被钉住，它和载体绑死，载体陪着睡。

JDK 21 的两个主要原因：
1. 阻塞发生在 `synchronized` 块/方法**里面**（或 `Object.wait()`）：JVM 的 monitor 实现把「谁持有锁」记在 **OS 线程**的栈帧上，拷走栈会让锁归属混乱，所以不卸载。
2. 栈上有 native 帧（JNI，或 FFM 下行调用回调 Java 再阻塞）。

文件 I/O 严格说不是 monitor 引起的 pin，而是「载体被占」，调度器靠多开载体补偿。
