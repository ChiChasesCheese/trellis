---
id: hl-j10-three-roles
node: java21.j10-virtual-threads
type: qa
step: 11
---
## Q
虚拟线程（virtual thread）、载体线程（carrier thread）、续体（continuation）三个角色分别是什么？

## A
- **虚拟线程**：一个普通 Java 对象（`java.lang.VirtualThread`），装着「一段可暂停的执行」。
- **载体线程**：真正的 OS 线程，数量很少，**默认等于核数**，属于一个专用 `ForkJoinPool`（即调度器）。输出里的 `ForkJoinPool-1-worker-1` 就是载体。
- **续体**：JVM 内部机制，能把线程当前整条调用栈**冻结**成堆上对象，以后**解冻**接着跑，这是虚拟线程的魔法所在。

只有载体线程是真 OS 线程；成千上万个虚拟线程多路复用在少数载体上。
