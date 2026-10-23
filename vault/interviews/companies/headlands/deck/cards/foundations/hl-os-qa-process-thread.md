---
id: hl-os-qa-process-thread
node: foundations.os-processes-threads-ipc
type: qa
step: 35
---
## Q
面试题：进程和线程的区别？

## A
推荐答法：「进程有独立虚拟地址空间，提供隔离，创建和切换成本高；线程共享所属进程的地址空间，只有各自的栈和寄存器，创建和切换便宜，但共享数据要同步，一个线程出错会拖垮整个进程。Linux 内核里两者都是 task，线程是共享地址空间的 task。Java 平台线程与内核线程 1:1；JDK 21 虚拟线程是 JVM 调度的用户态线程。」
