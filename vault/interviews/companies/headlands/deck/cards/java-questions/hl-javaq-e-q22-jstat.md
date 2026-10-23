---
id: hl-javaq-e-q22-jstat
node: java-questions.e-jit-gc
type: qa
step: 17
---
## Q
`jstat -gcutil <pid> 500` 的输出怎么读？G1、256 MB 堆、一个线程持续分配时，典型表现是什么？还有哪些观察 GC 的方式？

## A
列含义：S0/S1（Survivor 使用率）、E（Eden）、O（老年代）、M（元空间）、YGC / YGCT（young GC 次数 / 累计时间）、FGC / FGCT（Full GC）、GCT（总 GC 时间）。

示例：两次采样间隔 0.5 秒，YGC 从 1245 涨到 1685（每秒数百次 young GC），累计 GC 时间 0.27 → 0.37 秒，**FGC=0**，没有 Full GC——高分配率下 young GC 频繁但便宜。

其他观察：`-Xlog:gc*`、JFR、`jcmd <pid> GC.heap_info`、`GC.class_histogram`。
