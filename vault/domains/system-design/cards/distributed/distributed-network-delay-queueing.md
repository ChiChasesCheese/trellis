---
id: distributed-network-delay-queueing
node: distributed.time.failure
type: qa
---
## Q
Datacenter round trips are "sub-millisecond", yet your timeouts must tolerate delays thousands of times larger. Where does the variability in network delay actually come from, and what does that imply for choosing timeouts?

## A
Almost all of it is **queueing**, at every stage of the path:

- **Switch buffers** when several senders burst into one link (incast); overflow means drops, and TCP turns a drop into a **retransmission after a timeout** — milliseconds become hundreds of milliseconds.
- **The receiving OS** queues packets while all cores are busy; the receiving *application* may be GC-paused with data waiting in its socket.
- **Virtualization** queues a whole VM's packets while it's descheduled; TCP's own **flow/congestion control** queues data at the sender before it even leaves.

Queueing delay explodes near saturation (approaching infinity as utilization → 1), so delay is not just variable but **load-dependent**: yesterday's p999 is wrong during today's incident. Implications: timeouts must come from **continuously measured distributions** (or adaptive detectors), with headroom precisely when the system is busiest; and no fixed timeout can be "correct" — packet networks chose unbounded delay in exchange for high utilization (circuit networks make the opposite trade).

## Q zh
数据中心往返延迟号称"亚毫秒"，但你的超时必须容忍比这大几千倍的延迟。网络延迟的波动到底来自哪里？这对超时的选取意味着什么？

## A zh
几乎全部来自**排队**，发生在路径的每一段：

- **交换机缓冲区**：多个发送方同时向一条链路突发流量（incast）；缓冲溢出就丢包，而 TCP 把一次丢包变成**超时后的重传**——毫秒级延迟放大成几百毫秒。
- **接收端操作系统**在所有核都忙时把包排进队列；接收端*应用*可能正处于 GC 暂停，数据在 socket 里干等。
- **虚拟化**在 VM 被调度出去时把它的所有包排队；TCP 自己的**流控/拥塞控制**在数据离开发送端之前就先在发送侧排队。

排队延迟在接近饱和时爆炸（利用率趋近 1 时趋于无穷），所以延迟不仅波动，而且**依赖负载**：昨天的 p999 在今天的事故中就是错的。含义：超时必须来自**持续测量的分布**（或自适应探测器），并且恰恰要在系统最忙时留足余量；不存在"正确"的固定超时——分组交换网络用无界延迟换来了高利用率（电路交换网络做的是相反的交换）。
