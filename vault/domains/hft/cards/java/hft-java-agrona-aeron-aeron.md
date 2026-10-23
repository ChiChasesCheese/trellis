---
id: hft-java-agrona-aeron-aeron
node: java.agrona-aeron
type: qa
step: 2
---
## Q
Aeron 是什么？它的 Media Driver 和应用进程怎样分工，为什么这样设计？

## A
Aeron 是基于 UDP（单播或多播）和 IPC（同机共享内存）的低延迟消息传输，提供有序、可靠、流量控制，并带有 Archive（录制回放）和 Cluster（复制状态机）。

架构：应用进程里的 Aeron 客户端，把消息写进与 **Media Driver** 共享的内存映射文件（日志缓冲区），例如调用 `publication.offer(buffer, 0, 100)` 写 100 字节；Media Driver 是独立的进程（也可嵌入），负责真正收发 UDP 包、丢包重传和流控。

好处：应用线程只做内存写入，不进内核、不被网络 I/O 阻塞；应用即使遇到 GC 停顿，Driver 仍在继续收包和重传，不会丢数据；Driver 可以固定到专用核，还能换成内核旁路的实现。
