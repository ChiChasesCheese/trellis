---
id: hl-os-spsc-cross-process
node: foundations.os-processes-threads-ipc
type: qa
step: 31
---
## Q
跨两个 JVM 进程用 SPSC 环形缓冲传 5000 万条消息，吞吐是多少？为什么不比同进程两线程更慢？

## A
实测三次：消费者读 56.1、109.5、136.4 M msgs/s，生产者 0.89 s、0.46 s、0.37 s 写完 5000 万条，消费者校验每条都按顺序到达。波动来自两个进程被调度到哪两个核。

不更慢的原因：数据路径一样，都是缓存行在两个核之间传，**进程边界不介入**。
