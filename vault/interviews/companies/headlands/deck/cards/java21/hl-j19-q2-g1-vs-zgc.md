---
id: hl-j19-q2-g1-vs-zgc
node: java21.j19-runtime-zgc-jit
type: qa
step: 35
---
## Q
面试问：G1 和 ZGC 的区别是什么？
What is the difference between G1 and ZGC?

## A
- **G1**：在 **STW 暂停里做 evacuation**（复制存活对象），按暂停目标调节（默认 **200 ms**），暂停随要复制的活对象量增长；
- **ZGC**：**并发**标记和移动对象，用**着色指针 + 加载屏障**，暂停很短且**与堆大小无关**；
- **ZGC 的代价**：吞吐略低、GC 线程占更多 CPU、需要额外堆空间（headroom）避免 allocation stall。

英文骨架：「G1 evacuates inside stop-the-world pauses, so pause time scales with live data. ZGC relocates concurrently with colored pointers and load barriers, so pauses are tiny and independent of heap size. The price is lower throughput, more GC CPU and headroom.」
