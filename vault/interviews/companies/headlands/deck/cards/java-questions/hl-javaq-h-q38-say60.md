---
id: hl-javaq-h-q38-say60
node: java-questions.h-ipc
type: qa
step: 7
---
## Q
用英文 60 秒回答：What are the ways processes can communicate on one machine? Compare pipes, sockets, shared memory, message queues, files.

## A
结构：列出机制 → 管道与套接字经内核拷贝两次，共享内存零拷贝但要自己同步 → 实测往返 3、12、0.15 微秒 → 选型：套接字做通用与控制面，共享内存环形缓冲做同机微秒级延迟。

> "The main options are pipes, sockets including Unix domain sockets, shared memory, message queues, signals and files. Pipes and sockets go through the kernel and copy data twice; shared memory maps the same physical pages into both processes, so there's no copy and no syscall on the fast path, but you have to do your own synchronisation and handle a peer crashing mid-write. I measured round trips between two JVMs on my laptop: about 3 microseconds through a pipe, 12 through loopback TCP, and 0.15 through a memory-mapped file with spinning on a volatile sequence number. So I'd use sockets for generality and control traffic and shared-memory ring buffers when two processes on the same host need microsecond latency."
