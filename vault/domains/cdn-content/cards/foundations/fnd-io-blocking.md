---
id: fnd-io-blocking
node: foundations.os-io
type: qa
---
## Q
Why can one blocking disk or network operation stall thousands of requests in an event-driven proxy even when the machine has many cores?

## A
An event loop depends on handlers returning quickly. A blocking syscall parks the loop's thread, so ready sockets cannot be serviced and their queues grow; extra cores do nothing unless work is scheduled onto them. Use non-blocking I/O, bounded worker offload for unavoidable blocking work, and measure event-loop or scheduler delay—not only CPU.

## Q zh
为什么在多核机器上的 event-driven proxy 中，一个 blocking disk/network 操作仍能卡住几千个请求？

## A zh
event loop 依赖 handler 快速返回。blocking syscall 会挂起 loop 所在线程，让其他 ready socket 无法被处理、queue 持续增长；如果工作没有调度到其他核，多核也无济于事。使用 non-blocking I/O，对不可避免的 blocking work 使用有界 worker offload，并监控 event-loop/scheduler delay，而不只是 CPU。
