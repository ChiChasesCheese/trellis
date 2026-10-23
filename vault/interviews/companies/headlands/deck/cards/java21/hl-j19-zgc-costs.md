---
id: hl-j19-zgc-costs
node: java21.j19-runtime-zgc-jit
type: qa
step: 15
---
## Q
ZGC 的代价是什么？什么是 allocation stall？

## A
- 每次引用读取多一小段屏障 → **吞吐比 G1 略低**；
- 需要**额外堆空间**（headroom）：并发回收期间应用还在分配，新分配快过回收就发生 **allocation stall**（分配线程被迫等回收，成了新的延迟来源）；
- 并发工作占 CPU：GC 线程与应用线程抢核；
- 不用压缩指针，同样数据占更多内存。

所以堆太小、分配太快时，延迟反而可能不如 G1，要在你的负载上测。
