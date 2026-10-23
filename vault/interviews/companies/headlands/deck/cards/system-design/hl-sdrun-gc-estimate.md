---
id: hl-sdrun-gc-estimate
node: system-design.how-to-run
type: qa
step: 16
---
## Q
Java 的分配率与 GC 估算：每条消息 100 B 垃圾、100 万 msg/s，意味着什么？为什么「调好 GC」不是答案？

## A
- 分配率：100 B × 1M msg/s = **100 MB/s**；年轻代 1 GB 每 10 s 一次 minor GC。
- Parallel / G1 的 minor GC 停顿几 ms 到几十 ms（取决于存活对象），超出 10 µs 预算 **3 个数量级**。
- ZGC 把停顿压到亚毫秒（通常 < 1 ms），Shenandoah 通常 0–10 ms，但仍有读屏障、并发线程抢缓存 / CPU，对 µs 级热路径仍不够。

结论：稳态下**分配率必须约为 0**（对象复用、预分配、堆外），而不是调 GC。停顿的根因是分配，不是收集器。
