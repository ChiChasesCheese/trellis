---
id: pl-memana-found-java-dump
node: engineering.memory-analysis
type: qa
step: 3
---
## Q
Java 的堆转储（heap dump）、类直方图和保留大小（retained size）分别是什么？怎样获取和分析？

## A
**堆转储**是某一刻整个堆的完整快照：每个对象、字段和引用都在里面。获取：`jcmd <pid> GC.heap_dump file.hprof`；也可以加 `-XX:+HeapDumpOnOutOfMemoryError`，在内存溢出时自动落盘。转储前会触发一次 Full GC，应用在此期间暂停，文件大小约等于存活堆。

**类直方图**更轻：`jcmd <pid> GC.class_histogram` 按类聚合实例数与字节数，不含引用关系。对「3000 个 10 KB 数组放进一个静态 `HashMap` 缓存」的程序：

```text
 num     #instances         #bytes  class name
   1:         11481       30429440  [B (java.base)
```

`[B` 就是 `byte[]`，30 MB 都在字节数组上，指向缓存。

**分析工具**（Eclipse MAT、VisualVM、IntelliJ）里的几个概念：
- **浅大小**（shallow size）：对象自身占用；
- **保留大小**（retained size）：这个对象被回收时能连带释放的总量，即它独占持有的整个子图。保留大小才对应「修好它能省多少」；
- **支配树**（dominator tree）：如果从 GC 根到 B 的每条路径都经过 A，则 A 支配 B。按保留大小排序，一眼看到最大的持有者；
- **到 GC 根的路径**（path to GC roots）：对一个可疑对象，显示它为什么还活着。

不想整堆转储时，JFR 的 `jdk.OldObjectSample` 事件会持续采样仍存活的老对象，并可记录它们到 GC 根的路径，在线上就能找泄漏候选。
