---
id: hl-javaq-g-q35-nmt
node: java-questions.g-os
type: qa
step: 5
---
## Q
`-Xmx256m` 的 JVM，NativeMemoryTracking 显示进程驻留内存（RSS）大约多少？GC、线程、代码缓存各占多少？

## A
实测：
- 堆最大 256 MB，进程驻留内存约 **314 MB**（`ps -o rss=` 为 321808 KB）；NMT 总计 committed 约 419594 KB。
- Java Heap committed 225280 KB。
- **GC** 约 **58 MB**（G1 的记忆集、标记位图等簿记）。
- **线程**约 **68 MB**。
- Code：committed 7831 KB；共享类空间 12880 KB；Metaspace 3405 KB。
- 口径：RSS 里除堆之外，GC 簿记、线程、类空间、代码缓存都要算。
