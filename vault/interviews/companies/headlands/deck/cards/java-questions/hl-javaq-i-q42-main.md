---
id: hl-javaq-i-q42-main
node: java-questions.i-network
type: qa
step: 8
---
## Q
你会怎么降低交易或研究系统两个组件之间的网络延迟？
How would you reduce network latency between two components of a trading or research system?

## A
一句话：**先量，再减**。先量每一跳的延迟分布（p50 / p99 / p999，不是平均）；再减：少拷贝少序列化（二进制定长协议，不用 Java 序列化 / JSON）、一次 `write` 一条消息 + `TCP_NODELAY`、长连接、专用线程绑核忙轮询、缓冲区合理、避免 GC 与锁、必要时 UDP 多播 / 内核旁路。

延迟预算（量级，一般认识）：同机共享内存约 0.1–1 µs；同机 loopback TCP 约 10 µs（实测约 12 µs）；同机房网络一跳约 10–100 µs；跨城市约 ms。
