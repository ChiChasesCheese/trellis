---
id: hl-javaq-h-q38-numbers
node: java-questions.h-ipc
type: qa
step: 2
---
## Q
两个 JVM 进程做 5 万次往返 ping-pong，管道、loopback TCP、共享 mmap 每次往返各约多少微秒？共享内存的代价是什么？怎么选型？

## A
实测（macOS arm64）：
- 管道（stdin/stdout）：**3.08 µs**/往返。
- loopback TCP（NODELAY）：**12.32 µs**。
- 共享 mmap，自旋读 volatile 序号：**0.15 µs**。

共享内存比套接字快约**两个数量级**，因为不进内核、不拷贝；代价是**忙等占满一个核**。macOS 上管道比 loopback TCP 快（协议栈开销）；Linux 上顺序通常类似，数字不同。

选型：控制面 / 低频 → 套接字（或 gRPC）；同机高频、延迟敏感 → 共享内存环形缓冲；父子进程简单管道 → `ProcessBuilder`。
