---
id: hft-java-at-hft-interop-shared-memory
node: java-at-hft.interop
type: qa
step: 2
---
## Q
同一台机器上的 C++ 进程和 Java 进程，怎样用共享内存队列交换消息？为什么比 socket 快？

## A
做法：两个进程把同一个文件映射进各自的地址空间（通常放在内存文件系统 `/dev/shm`），在里面放一个**环形缓冲区**加头尾序号。生产者先写数据，再用 release 语义写序号；消费者用 acquire 语义读序号，再读数据。两边的内存序约定必须一致：C++ 的 `std::atomic` release/acquire 对应 Java 的 `VarHandle` `setRelease`/`getAcquire`。

比 socket 快是因为：没有系统调用，没有内核里的协议栈和拷贝。量级上，共享内存的一次传递是亚微秒到数微秒，本机回环 TCP 通常是十几到几十微秒。Aeron 的 IPC 模式、Chronicle Queue 都是这个思路。

限制：只能同机，内存布局（对齐、缓存行填充）要两边严格一致，进程崩溃后遗留的状态要有恢复办法。
