---
id: hl-javaq-f-q31-numbers
node: java-questions.f-concurrency
type: qa
step: 22
---
## Q
12 核机器上，1 万和 10 万个各阻塞 1 秒的虚拟线程总共需要多久？同样的任务用 200 线程的平台池做 2000 个要多久？

## A
- 10,000 个虚拟线程各阻塞 1 s：完成用时 **1195 ms**。
- 100,000 个：**1592 ms**（几乎全并行）。
- 200 线程的平台池做 2000 个任务：**11281 ms**（= 2000/200 × 1 s，吞吐被线程数卡住）。
- 虚拟线程的线程名形如 `VirtualThread[#20,v1]/runnable@ForkJoinPool-1-worker-1`，说明运行在 ForkJoinPool 的载体线程上。
- 不要池化虚拟线程（它们本来就便宜），限并发用 `Semaphore`。
