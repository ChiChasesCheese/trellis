---
id: hl-javaq-i-q41-say60
node: java-questions.i-network
type: qa
step: 12
---
## Q
用英文 60 秒回答：Blocking I/O vs NIO vs epoll vs Netty vs virtual threads: how do you serve many connections? What does `read()` do inside the kernel?

## A
结构：三种模型（每连接一线程、反应器、虚拟线程）→ epoll 只返回就绪描述符，优于 select 和 poll → 最低延迟仍用手写的绑核单线程事件循环。

> "There are three models. Thread-per-connection with blocking I/O is simplest but limited by thread count and context-switch cost. The reactor model uses a few threads, each running a selector loop - in Java `Selector`, backed by epoll on Linux - that waits until sockets are ready and then does non-blocking reads and writes; Netty is built on that. `epoll` beats `select` and `poll` because it returns only ready descriptors instead of scanning all of them. With Java 21 virtual threads I can write the simple blocking style again and the JDK multiplexes underneath. For the very lowest latency I'd still use a hand-written single-threaded event loop pinned to a core with direct buffers, because nothing in it can block or be descheduled by anything else."
