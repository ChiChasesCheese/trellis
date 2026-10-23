---
id: hl-sdrun-jitter-sources
node: system-design.how-to-run
type: qa
step: 20
---
## Q
延迟抖动（jitter）的来源清单有哪些？

## A
可逐条念：
- GC 停顿 / safepoint；
- JIT 反优化（deopt）与编译线程；
- 缺页（page fault）、透明大页压缩（THP compaction）；
- 中断、`irqbalance`；
- 同核心超线程（SMT）兄弟；
- NUMA 远端内存；
- CPU 降频 / C-state 唤醒；
- 其他进程抢占；
- 日志 / 监控线程争用缓存；
- Nagle / 延迟确认；
- 虚拟化环境下 `System.nanoTime()` 变慢。
