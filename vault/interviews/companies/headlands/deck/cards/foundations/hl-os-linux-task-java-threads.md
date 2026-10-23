---
id: hl-os-linux-task-java-threads
node: foundations.os-processes-threads-ipc
type: qa
step: 4
---
## Q
Linux 内核怎么看待线程？Java 的平台线程和虚拟线程与内核线程是什么对应关系？

## A
Linux 内核里进程和线程都叫 **task**。线程是用 `clone(CLONE_VM | CLONE_FILES | …)` 创建的、**与创建者共享地址空间**的 task。`ps -eLf` 看每个线程，`top -H` 按线程显示。

Java：
- 一个 JVM = 一个进程；
- **平台线程**（`new Thread(...)` 或线程池里的线程）与内核线程 **1:1**，各有内核栈和 Java 栈（默认约 1 MB，`-Xss` 调整），几千个就是极限；
- **虚拟线程**（JDK 21 正式）：JVM 调度、挂在少量平台线程（载体 carrier）上，遇到阻塞 I/O 让出载体；适合大量、等待居多的任务，**不**适合 CPU 密集。
