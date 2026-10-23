---
id: hl-j10-gc-thread-dump
node: java21.j10-virtual-threads
type: qa
step: 25
---
## Q
大量活跃虚拟线程对 GC 有什么影响？为什么 `jstack` 看不到虚拟线程，应该用什么命令做线程转储？

## A
- **GC**：每个虚拟线程的栈是堆对象。几十万个活跃虚拟线程各带几 KB 栈，堆压力和 GC 扫描都增加，用 ZGC/G1 调堆时要考虑。
- **线程转储**：`jstack` 看不到虚拟线程。用 JDK 21 新增的
  `jcmd <pid> Thread.dump_to_file -format=json <file>`。
