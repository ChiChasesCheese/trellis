---
id: hl-javaq-i-q42-say60
node: java-questions.i-network
type: qa
step: 13
---
## Q
用英文 60 秒回答：How would you reduce network latency between two components of a trading or research system?

## A
结构：先按分位数测每一跳 → 按收益排序的措施（二进制协议、一次 write 加 NODELAY 与长连接、绑核忙轮询线程、缓冲区、UDP 多播与内核旁路）→ 内核旁路处交给 C++ → 每次改动后重新测。

> "First I'd measure per-hop latency as percentiles so I know where the time goes. Then, in order of payoff: a compact fixed-layout binary protocol with no per-message allocation or Java serialization; one write per message with `TCP_NODELAY` over a long-lived connection; a dedicated networking thread that busy-polls instead of sleeping, pinned to an isolated core, with the GC and other threads kept off it; sensible socket buffers; and where it matters, UDP multicast for fan-out and kernel-bypass stacks. That last part is where I'd expect to hand over to C++ or vendor libraries, since Java's tooling there is thinner. And I'd re-measure after every change rather than trust folklore."
