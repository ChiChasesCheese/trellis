---
id: hl-j19-pitfalls-misc
node: java21.j19-runtime-zgc-jit
type: qa
step: 31
---
## Q
GC 调参有哪些坑（货物崇拜、虚拟线程、观测方式）？

## A
- **GC 调参有「货物崇拜」风险**：从网上抄一串 `-XX:` 标志却不知其作用。先测量（`-Xlog:gc`、JFR），再**一次改一个变量**。
- **虚拟线程的栈在堆上**：大量活跃虚拟线程增加堆压力与 GC 扫描量。
- **ZGC 不是白送的**：吞吐略降、需额外堆空间和 CPU、不用压缩指针；堆太小、分配太快 → allocation stall，延迟反而不如 G1。
- JDK 21 里别忘了 `-XX:+ZGenerational`；`-Xms` 与 `-Xmx` 设成一样并加 `-XX:+AlwaysPreTouch`。
