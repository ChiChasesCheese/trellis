---
id: hl-javaq-f-q27-pinning
node: java-questions.f-concurrency
type: qa
step: 9
---
## Q
什么是虚拟线程的 pinning？在只留 1 个载体线程、8 个任务各睡 200 ms 的实验里，`synchronized` 内外的耗时差多少？怎么规避、怎么观察？

## A
- **pinning**：JDK 21 里虚拟线程在 `synchronized` 内阻塞时，无法卸载，**钉住载体线程**。
- 实验：`sleep inside synchronized` **2455 ms**（载体被钉住，8 个任务近似串行，理想串行 1600 ms 加调度开销）；`sleep outside synchronized` **348 ms**（睡眠时虚拟线程让出载体，近似并行，理想 200 ms）。
- **规避**：对"可能阻塞"的临界区用 `ReentrantLock`，避免在 `synchronized` 里做 I/O / 睡眠。该限制由 JDK 24 的 JEP 491 取消。
- **观察**：`-Djdk.tracePinnedThreads=full` 打印 pin 事件。
