---
id: hl-j10-cooperative-scheduling
node: java21.j10-virtual-threads
type: qa
step: 16
---
## Q
虚拟线程的调度是协作式（cooperative）还是抢占式（preemptive）？这对纯计算的虚拟线程意味着什么？

## A
**协作式**。OS 线程可被 OS 随时打断（时间片到），而虚拟线程**只有主动阻塞（park）时才让出载体**。

后果：一个纯计算循环 100 亿次的虚拟线程会一直霸占载体直到算完，没有时间片抢占；载体只有核数个，被这样的线程占满，其他虚拟线程就得不到运行。所以死循环或长计算不适合放在虚拟线程里。
