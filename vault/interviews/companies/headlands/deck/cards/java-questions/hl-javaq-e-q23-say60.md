---
id: hl-javaq-e-q23-say60
node: java-questions.e-jit-gc
type: qa
step: 32
---
## Q
用英文 60 秒回答：Your Java trading component has latency spikes. How do you choose and tune the GC? When ZGC, when G1?

## A
结构：先测量不要先调参 → 降分配率是最大杠杆 → 选收集器（低延迟大堆用分代 ZGC，吞吐用 G1）→ 固定堆与预触碰 → 每次改动后用日志确认。

> "I'd start by measuring, not tuning: unified GC and safepoint logging, aligned with the latency spikes, to see whether the spikes are really GC pauses. If they are, the biggest lever is reducing allocation rate on the hot path - primitives, no boxing, reuse. Then collector choice: for latency-sensitive services with big heaps I'd use generational ZGC, which keeps pauses sub-millisecond - in my test, 0.14 ms versus 8 ms for G1 and 22 ms for Parallel - and keep the heap fixed-size with headroom and pre-touched. G1 is fine when a few milliseconds of pause are acceptable and throughput matters more. And I'd confirm with logs after each change instead of tuning by folklore."
